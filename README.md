# CoC-DASS

Developed a Clash of Clans inspired game in python exploiting the advantages of Object Oriented Programming Concepts. Implemented different types of troops, user-controlled and automatic, with attack and special abilities, and various defence buildings which can identify and target enemy troops.

This is a 2D terminal based interactive game, where the user can control the movement of the main troop, the king, and can also deploy troops of different kinds such as barbarians and archers.

Some of the ways in which OOPS concepts have helped build this game are:
- Inheritance: Different buildings (wall, wizard tower, cannon, etc) have been inherited from the common building class. (see [building.py](./src/building.py)). Similarly, different troops have been inherited from a common troop class. (see [troop.py](./src/troop.py))

- Encapsulation: The troops and buildings have different features and abilities which have been coded as functions in a class. This reflects encapsulation.

- Abstraction: The controls of the troops like move and attack are managed by functions called move() and attack(). This abstracts away teh details. 

- Polymorphism: Since all the troops are inherited from a common troop class, but different troops have varying movement rules, we have employed function overloading to use the same name for different functionalities!

To play the game: 

```
$ python3 game.py
```

Enjoy!!