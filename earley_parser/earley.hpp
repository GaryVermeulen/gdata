#ifndef EARLEY_HPP
#define EARLEY_HPP
 
#include <string>
#include <vector>
#include <list>
#include <iostream>
#include <iterator>
#include <algorithm>
 
#include "grammar.hpp"
 
namespace MB
{
 
namespace detail
{
 
// An element of a statelist, also known as a "dotted rule" or "Earley item"
struct state
{
    MB::rule::const_ptr rule_; // The grammar rule
    const unsigned int right_; // Index of right hand side alternative
    unsigned int dot_; // Position of dot within symbols on right hand side
    unsigned int i_, j_; // Positions within the input
    char added_by_; // Which function added this state
    state(MB::rule::const_ptr rule, unsigned int right, unsigned int i, unsigned int j)
        : rule_(rule), right_(right), dot_(0), i_(i), j_(j), added_by_(0)
    {
    }
 
    // Is dot all the way to the right?
    bool completed() const
    {
        return dot_ == rule_->right()[right_].size();
    }
 
    // Get symbol to the right of dot
    std::string next_symbol() const
    {
        return rule_->right()[right_][dot_];
    }
};
 
// Pretty-print state
std::ostream& operator <<(std::ostream& os, const state& st)
{
    const std::vector<std::string>& right = st.rule_->right()[st.right_];
    size_t rlen = right.size();
    os << '(';
    os << st.rule_->left() << " -> ";
    unsigned int s;
    for (s = 0; s < rlen; ++s) {
        if (s == st.dot_) {
            os << "@ ";
        }
        os << right[s];
        if (s < rlen - 1) {
            os << ' ';
        }
    }
    if (s == st.dot_) {
        os << " @";
    }
    os << ", [" << st.i_ << " , " << st.j_ << "]) ";
    switch (st.added_by_) {
        case 'P':
            os << "predictor";
            break;
        case 'S':
            os << "scanner";
            break;
        case 'C':
            os << "completer";
            break;
        default:
            os << "start state";
    }
    return os;
}
 
// Needed to check for duplicate states
bool operator ==(const state& state1, const state& state2)
{
    return state1.rule_->left() == state2.rule_->left()
        && state1.rule_->right() == state2.rule_->right()
        && state1.right_ == state2.right_
        && state1.dot_ == state2.dot_
        && state1.i_ == state2.i_
        && state1.j_ == state2.j_;
}
 
// A statelist is a list of states
typedef std::list<state> statelist;
 
// A chart is a vector of statelists
struct chart
{
    const MB::grammar& grammar_;
    std::vector<statelist> chart_;
 
    chart(const MB::grammar& grammar)
        : grammar_(grammar),
        // Chart begins with 1 statelist containing 1 dummy state used to track
        // successful parse
        chart_(1, statelist(1, state(MB::rule::create("$", grammar.get_start_left()),
                        0, 0, 0)))
    {
    }
 
    // Add state st to statelist s
    void add_state(state& st, unsigned int s)
    {
        if (s < chart_.size()) {
            // Adding to the last statelist
            statelist::iterator it = std::find(chart_[s].begin(), chart_[s].end(), st);
            if (it == chart_[s].end()) {
                chart_[s].push_back(st);
            }
        }
        else {
            // Adding to a new statelist
            chart_.push_back(statelist(1, st));
        }
    }
 
    // Add predictions for the next symbol in this state
    void predictor(state& st)
    {
        std::vector<MB::rule::const_ptr> rules;
        grammar_.get_rules_for_left(st.next_symbol(), std::back_inserter(rules));
        for (MB::rule::const_ptr r : rules) {
            for (unsigned int a = 0; a < r->right().size(); ++a) {
                state prediction = state(r, a, st.j_, st.j_);
                prediction.added_by_ = 'P';
                add_state(prediction, st.j_);
            }
        }
    }
 
    // Scan input for next symbol
    void scanner(const state& st, const std::vector<std::string>& input)
    {
        const std::string& word = input[st.j_];
        if (word == st.rule_->right()[st.right_][st.dot_]) {
            state scanned = state(st.rule_, st.right_, st.i_, st.j_ + 1);
            scanned.dot_ = st.dot_ + 1;
            scanned.added_by_ = 'S';
            add_state(scanned, st.j_ + 1);
        }
    }
 
    // Complete states
    void completer(const state& st)
    {
        const statelist& list = chart_[st.i_];
        const unsigned int i = st.i_;
        const unsigned int j = st.j_;
        for (const state& candidate : list) {
            if (candidate.j_ == i
                    && !candidate.completed()
                    && candidate.next_symbol() == st.rule_->left())
            {
                state completed = state(candidate.rule_, candidate.right_, candidate.i_, j);
                completed.dot_ = candidate.dot_ + 1;
                completed.added_by_ = 'C';
                add_state(completed, j);
            }
        }
    }
 
    // We have succeeded if the completed dummy state is in the final statelist
    bool succeeded() const
    {
        const statelist& list = chart_[chart_.size() - 1];
        return std::find_if(list.begin(), list.end(),
                [](const state &st)->bool {
                return st.rule_->left() == "$" && st.completed(); })
            != list.end();
    }
 
    // The main algorithm
    bool parse(const std::vector<std::string>& input, std::ostream *os)
    {
        for (unsigned int i = 0; i <= input.size(); ++i) {
            if (chart_.size() > i) { // Check for running out of statelists when parse fails
                for (statelist::iterator it = chart_[i].begin(); it != chart_[i].end(); ++it) {
                    state& st = *it;
                    if (!st.completed()
                            && !grammar_.symbol_is_terminal(st.next_symbol())) {
                        predictor(st);
                    }
                    else if (!st.completed()) {
                        if (i < input.size()) {
                            scanner(st, input);
                        }
                    }
                    else {
                        completer(st);
                    }
                }
                if (os) {
                    *os << *this;
                    *os << '\n';
                }
            }
        }
        return succeeded();
    }
 
    // Pretty-print chart
    friend std::ostream& operator <<(std::ostream& os, const chart &ch)
    {
        for (unsigned int i = 0; i < ch.chart_.size(); ++i) {
            os << "S" << i << ": ";
            os << '[';
            unsigned int j = 0;
            for (const state& st : ch.chart_[i]) {
                os << st;
                if (j < ch.chart_[i].size() - 1) {
                    os << ",\n";
                }
                ++j;
            }
            os << ']';
            os << "\n\n";
        }
        return os;
    }
};
 
} // namespace detail
 
class earley_parser
{
public:
    earley_parser(const MB::grammar& grammar)
        : grammar_(grammar)
    {
    }
    template <class InputIt>
    bool parse(InputIt begin, InputIt end) const
    {
        std::vector<std::string> input;
        std::copy(begin, end, std::back_inserter(input));
        return detail::chart(grammar_).parse(input, nullptr);
    }
    template <class InputIt>
    bool parse(InputIt begin, InputIt end, std::ostream& os) const
    {
        std::vector<std::string> input;
        std::copy(begin, end, std::back_inserter(input));
        return detail::chart(grammar_).parse(input, &os);
    }
private:
    const MB::grammar& grammar_;
};
 
} // namespace MB
 
#endif // EARLEY_HPP