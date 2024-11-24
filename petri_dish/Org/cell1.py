# cell1.py
#

from cell2 import cell2

def cell1(cell_input):

    from cell2 import cell2

    print("I am function cell1")
    cell_output = str(cell_input) + " concat cell1"

    print(cell2("cell1 function input")) 


    return cell_output


if __name__ == "__main__":

    print("I am cell1")
    print(cell1("cell1"))

    print(cell2("input_from_cell1"))
