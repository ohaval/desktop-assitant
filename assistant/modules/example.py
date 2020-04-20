import sys; sys.path.append("..")

from assitant import Assitant


class Example(Assitant):
    # You can define class variables here.

    def start(self):
        # Add here your GUI objects to the main object. (Buttons, Text Boxes, etc..)
        # It is recommended to use self.add_button(text, func) for better gui optimization.

        self.root.mainloop()

    # You can create functions here to be called.


def main():
    # Running the instance and starting the application.
    obj = Example()
    obj.start()


if __name__ == "__main__":
    main()
