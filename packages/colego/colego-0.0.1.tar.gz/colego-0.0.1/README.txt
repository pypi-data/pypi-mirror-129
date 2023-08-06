##################DESCRIPT#######################

This is a very simple package that converts a text to have colors in a terminal output.
Available colors: grey, red, green, yellow, blue, purple, cyan, white.
Three methods: txtcolor(), bgcolor(), complrandom() -> all of them returns a string.

Note: This package is still being worked on as the colors only works on specific terminals, one of them which is VSC's terminal.
Note: There is a bug where you can't use start_index and stop_index with random set to True.

##################EXAMPLES#######################

Two examples of a txtcolor():
    # Example 1:
        print(txtcolor(text="Hello World!", random=True)) # each character will have a random color

    # Example 2:
        print(txtcolor(text="Hello World!", color="red", start_index=3, stop_index=7, bold=True))

Two examples of bgcolor():
    # Example 1:
        print(bgcolor(text="Hello World!", random=True))

    # Example 2:
        print(txtcolor(text="Hello World!", color="blue", start_index=3, stop_index=7))

One example of complrandom():
    # Example 1:
        print(complrandom(text="Hello World!"))

#################################################