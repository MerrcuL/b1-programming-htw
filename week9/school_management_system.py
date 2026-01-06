class Person:
    """Base class representing a person with a name and age."""
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."

class Student(Person):
    """Student class inheriting from Person, including a student ID."""
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    def introduce(self):
        return f"Hi, I'm {self.name}, a student (ID: {self.student_id}) aged {self.age}."

class Teacher(Person):
    """Teacher class inheriting from Person, including a teaching subject."""
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def introduce(self):
        return f"Good morning, I am {self.name}. I teach {self.subject} and I am {self.age} years old."

def main():
    student = Student("Alice", 16, "S001")
    teacher = Teacher("Mr. Smith", 35, "Mathematics")

    print("--- School Management System Test ---")
    print(student.introduce())
    print(teacher.introduce())

if __name__ == "__main__":
    main()