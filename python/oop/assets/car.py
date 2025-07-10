class Car:
    def __init__(self, model, year, color, is_for_sale):
        self.model = model
        self.year = year
        self.color = color
        self.is_for_sale = is_for_sale

    def drive(self):
        print(f"I am driving the {self.color} {self.model}")
    
    def stop(self):
        print(f"I am stopping the {self.color} {self.model}")

    def describe(sellf):
        print(f"This is a car with {self.model} {self.year} model, \
            with color: {self.color}, and is for sale: {self.is_for_sale}")


