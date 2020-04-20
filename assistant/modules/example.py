import sys; sys.path.append("..")
from assistant.assitant import Assitant


class Example(Assitant):
    # You can define class variables here.

    def start(self):
        # Add here your GUI objects to the main object. (Buttons, Text Boxes, etc..)

        self.root.mainloop()

    # You can create functions here to be called.


def main():
    # Running the instance and starting the application.
    obj = Example()
    obj.start()


if __name__ == "__main__":
    main()
