from ..assitant import Assitant


class Example(Assitant):
    # You can define class variables here.

    def start(self):
        # Add here your GUI objects to the main object. (Buttons, Text Boxes, etc..)

        self.root.mainloop()

    # You can create functions here to be called.


# Running the instance and starting the application.
obj = Example()
obj.start()
