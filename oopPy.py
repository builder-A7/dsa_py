# Python OOP Concepts Demonstration

# --- Concept: Abstraction (defining a conceptual interface) ---
# --- Concept: Class (blueprint for objects) ---
# --- Concept: Constructor (__init__) ---
# --- Concept: Instance Variables (e.g., self._title) ---
# --- Concept: Encapsulation (bundling data and methods, _protected members) ---
# --- Concept: Properties (@property, @setter, @deleter for controlled access) ---
# --- Concept: Special/Magic Methods (e.g., __str__) ---

class MediaItem:
    """
    Represents a generic media item.
    Demonstrates: Class, Object (when instantiated), __init__, instance variables,
                  Encapsulation (_title), Properties, Abstraction (base for other types),
                  Special methods (__str__).
    """
    def __init__(self, title, item_type="Generic Media"):
        self._title = title             # Protected instance variable
        self._item_type = item_type     # Protected instance variable

    @property
    def title(self):
        # Getter for title
        return self._title

    @title.setter
    def title(self, value):
        # Setter for title with validation
        if not value:
            print("Error: Title cannot be empty.")
        else:
            self._title = value

    @title.deleter
    def title(self):
        # Deleter for title
        print(f"Deleting title for '{self._title}'...")
        self._title = "N/A" # Or del self._title if appropriate, depending on design

    def get_info(self):
        # Abstract-like method, intended to be overridden by subclasses
        return f"This is a {self._item_type}."

    def __str__(self):
        # String representation of the object
        return f"'{self.title}' ({self._item_type})"

# --- Concept: Inheritance (Single Inheritance: Book inherits from MediaItem) ---
# --- Concept: Method Overriding (get_info, __str__ in Book) ---
# --- Concept: super() (to call parent class methods) ---
# --- Concept: More Instance Variables (self.author, self.pages) ---
# --- Concept: Operator Overloading (e.g., __len__, __add__) ---
# --- Concept: Destructor (__del__) ---
class Book(MediaItem):
    """
    Represents a book, inheriting from MediaItem.
    Demonstrates: Single Inheritance, Method Overriding, super(), more instance variables,
                  Operator Overloading (__len__, __add__), Destructor (__del__).
    """
    def __init__(self, title, author, pages):
        super().__init__(title, item_type="Book") # Call parent's __init__
        self.author = author # Instance variable specific to Book
        self._pages = pages   # Protected instance variable

    def get_info(self): # Overriding parent's method
        base_info = super().get_info() # Calling parent's method
        return f"{self.title} by {self.author}, {self._pages} pages. ({base_info})"

    def __str__(self): # Overriding parent's method
        return f"Book: '{self.title}' by {self.author} ({self._pages} pages)"

    def __len__(self): # Operator overloading for len()
        return self._pages

    def __add__(self, other_book): # Operator overloading for +
        if isinstance(other_book, Book):
            return Book(f"{self.title} & {other_book.title} Collection",
                        f"{self.author} & {other_book.author}",
                        self._pages + other_book._pages)
        return NotImplemented # Important for binary operations

    def __del__(self):
        # Called when the object is about to be garbage collected.
        # Use with caution, primarily for releasing external resources.
        # Python's garbage collector handles memory automatically.
        # print(f"Book '{self.title}' is being finalized/destroyed.")
        pass


# --- Concept: Class Variables (shared among all instances of a class) ---
# --- Concept: Class Methods (@classmethod: operates on the class itself) ---
# --- Concept: Static Methods (@staticmethod: utility function, no access to cls or self) ---
class Library:
    """
    Represents a library.
    Demonstrates: Class Variables, Class Methods, Static Methods.
    """
    # Class variable
    opening_hours = "9 AM - 5 PM"
    all_libraries = [] # Another class variable

    def __init__(self, name):
        self.name = name # Instance variable
        self.catalog = [] # Instance variable (list of MediaItem objects)
        Library.all_libraries.append(self)

    def add_item(self, item):
        if isinstance(item, MediaItem):
            self.catalog.append(item)
        else:
            print("Error: Can only add MediaItem objects to catalog.")

    @classmethod
    def get_opening_hours(cls): # Class method
        return f"All libraries are open: {cls.opening_hours}"

    @classmethod
    def create_branch_library(cls, branch_name): # Class method as a factory
        print(f"Creating a new branch of type {cls.__name__}: {branch_name}")
        return cls(branch_name) # Creates an instance of the class (or subclass)

    @staticmethod
    def is_valid_library_name(name): # Static method
        return isinstance(name, str) and len(name) > 2

    def __str__(self):
        return f"Library: {self.name}, Catalog Size: {len(self.catalog)}"

# --- Concept: Multiple Inheritance (AudioBook inherits from Book and a new Mixin) ---
# A Mixin class (often provides specific functionality)
class Playable:
    """
    A mixin class for items that can be played.
    Demonstrates: A common use case for Multiple Inheritance (providing reusable methods).
                  Encapsulation (_is_playing).
    """
    def __init__(self, duration_minutes): # Mixins can have __init__
        self._duration_minutes = duration_minutes
        self._is_playing = False # Encapsulated state

    def play(self):
        if hasattr(self, 'title'): # Check if it's mixed into something with a title
            print(f"Playing '{self.title}'...")
        else:
            print("Playing media...")
        self._is_playing = True

    def stop(self):
        print("Stopping media.")
        self._is_playing = False

    def get_duration(self):
        return f"{self._duration_minutes} minutes"


class AudioBook(Book, Playable): # Multiple Inheritance
    """
    Represents an audiobook, inheriting from Book and Playable.
    Demonstrates: Multiple Inheritance, calling __init__ of multiple parents.
    """
    def __init__(self, title, author, pages, duration_minutes, narrator):
        Book.__init__(self, title, author, pages) # Call Book's __init__
        Playable.__init__(self, duration_minutes) # Call Playable's __init__
        self.narrator = narrator
        # Override item_type if necessary (from MediaItem, via Book)
        self._item_type = "AudioBook" # Example of accessing protected member of grandparent

    def get_info(self): # Further overriding
        book_info = Book.get_info(self) # Can explicitly call specific parent method
        return f"{book_info}\nNarrated by: {self.narrator}. Duration: {self.get_duration()}."

    def __str__(self): # Overriding
        return f"AudioBook: '{self.title}' by {self.author}, Narrator: {self.narrator}"


# --- Concept: Polymorphism ---
# Polymorphism allows objects of different classes to respond to the same method call.
# 1. Duck Typing: If it quacks like a duck and walks like a duck, it's a duck.
#    The `process_media` function doesn't care about the actual class type,
#    only that the object has a `get_info()` method and can be printed (has `__str__`).
# 2. Through Inheritance/Method Overriding: `get_info()` is implemented differently
#    by `MediaItem`, `Book`, and `AudioBook`.

def process_media_item(media_item: MediaItem): # Type hint for clarity, but not strictly enforced by duck typing
    """Demonstrates polymorphism."""
    print("\n--- Processing Media Item ---")
    print(media_item)         # Calls __str__ method of the specific object
    print(media_item.get_info()) # Calls get_info method of the specific object
    if isinstance(media_item, Playable): # Specific check for Playable behavior
        media_item.play()
        media_item.stop()

# --- Instantiation (Creating Objects) & Demonstration ---

# MediaItem Object
generic_media = MediaItem("Generic Film Reel")

# Book Objects
book1 = Book("The Lord of the Rings", "J.R.R. Tolkien", 1200)
book2 = Book("1984", "George Orwell", 328)

# AudioBook Object
audio_book1 = AudioBook("Dune", "Frank Herbert", 500, 1260, "Scott Brick")

# Library Objects
main_library = Library("City Central Library")
main_library.add_item(book1)
main_library.add_item(audio_book1)

# --- Demonstrating Encapsulation & Properties ---
print(f"\nOriginal title: {generic_media.title}")
generic_media.title = "A Classic Film" # Using setter
print(f"Updated title: {generic_media.title}")
del generic_media.title # Using deleter
print(f"After deleting title: {generic_media.title}")
generic_media.title = "Restored Classic Film" # Set it back

# --- Demonstrating Inheritance, Method Overriding, super() ---
# (Demonstrated by process_media_item calls below)

# --- Demonstrating Operator Overloading ---
print(f"\nPages in '{book1.title}': {len(book1)}") # Calls book1.__len__()
book_collection = book1 + book2                   # Calls book1.__add__(book2)
if book_collection:
    print(f"Combined book: {book_collection.title}, Pages: {len(book_collection)}")

# --- Demonstrating Class/Static Methods ---
print(f"\nLibrary Info: {Library.get_opening_hours()}") # Calling class method
print(f"Is 'Main St Library' a valid name? {Library.is_valid_library_name('Main St Library')}") # Calling static method
branch_library = Library.create_branch_library("Oak Street Branch") # Factory using class method
print(branch_library)
print(f"Total libraries created: {len(Library.all_libraries)}")


# --- Demonstrating Multiple Inheritance & Polymorphism ---
process_media_item(generic_media) # MediaItem object
process_media_item(book1)         # Book object
process_media_item(audio_book1)   # AudioBook object (also Playable)

# The `__del__` methods for book1, book2, audio_book1 etc. will be called
# when these objects are no longer referenced and Python's garbage collector reclaims them.
# This usually happens when the script ends or if `del` is used explicitly and
# no other references exist.
print("\n--- End of Script ---")