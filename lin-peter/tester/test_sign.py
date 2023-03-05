from sign import sign
import os
import csv


def setup():
    mock_input_stream = [num for num in range(1, 4, 1)]
    mock_output_stream = [1]*3
    if not os.path.isfile("mock_input.csv"):
        with open("mock_input.csv", "w") as file:
            file.write(",".join(str(item) for item in mock_input_stream))
    if not os.path.isfile(r"mock_output.csv"):
        with open("mock_output.csv", "w") as file:
            file.write(",".join(str(item) for item in mock_output_stream))
    print("setup completed")


def test_sign_negative():
    assert sign(-3) == -1


def test_sign_positive():
    assert sign(19) == 1


def test_sign_zero():
    """test:assert"""
    assert sign(0) == 0


# Misspelled 'sign'
def test_sign_error():
    assert sgn(1) == 1


test_sign_error.skip = True


def test_sign_input():
    with open("mock_input.csv", "r") as input_file:
        input_csv = csv.reader(input_file)
        for row in input_csv:
            input_list = [int(entry) for entry in row]

    with open("mock_output.csv", "r") as output_file:
        output_csv = csv.reader(output_file)
        for row in output_csv:
            output_list = [int(entry) for entry in row]

    for input_num, output_num in zip(input_list, output_list):
        assert sign(input_num) == output_num


def teardown():
    if os.path.isfile("mock_input.csv"):
        os.remove("mock_input.csv")
        print("mock input file removed")

    if os.path.isfile("mock_output.csv"):
        os.remove("mock_output.csv")
        print("mock output file removed")

    print("tear down completed")

