c4 - a Python Connect-Four Player
=================================

Simple Python library with some implementations of algorithms used to
play `zero-sum games`_.

Some of the algorithms implemented:
* `Negamax`_
* `Alpha beta pruning`_
* `Principal variation search`_ (Negascout)
* `Transposition table`_
* `Iterative deepening`_

The aim is to show the effectiveness of these algorithms in a simple context like
the game of connect-four.

These very same algorithms can be used in all other zero-sum games like Chess, Xiangqi,
Shogi, Go, etc...

All these algorithms will be explained with more details in my blog:
http://blogs.skicelab.com/maurizio/

My series of post dedicated to Chess programming and zero sum based games are here:
http://blogs.skicelab.com/maurizio/category/chess.html


Requirements
------------

* Python 3
* numpy


Commands
--------

The ``run`` script has some commands that can be executed by the command line.

.. code-block:: sh

    ./run COMMAND [OPTIONS]

Use ``./run --help`` to have a list of commands.


Game
~~~~

You can play using the ``game`` command::

    ./run game greedy

This will let you play against the ``greedy`` engine. To see the list of
engines you can play with check `Engines`_.

Use the ``--player2`` option to play as the player 2.


Arena
~~~~~

The ``arena`` command runs a tournament between artificial players.
You need to setup a yaml file with the options of the player as the following:

.. code-block:: yaml

    - class: greedy
    - class: pvsdeep
      maxdepth: 6

This creates a tournament with 2 players, one that uses the `greedy` engine
an the other one that uses PVS, Transposition tables and Iterative Deepening with
a maximum search depth of 6.

Check `Engines`_ to know the list of the allowed engine class names with their options.


Bestmove
~~~~~~~~

A quick overview of the engine performance can be given by executing the ``bm`` command
that just run the engine on the empty board to choose the first bestmove.

The arguments of this command are very similar to the ``game`` command.


Engines
-------

These are the engines supported for the ``arena``, ``bm`` and ``game`` commands:


``greedy``
  Simple greedy search.

``negamax``
  Negamax search algorithm.

``alphabeta``
  Alpha-Beta pruning search algorithm.

``abcached``
  Alpha-Beta with transposition table.

``abdeep``
  Alpha-Beta with Iterative Deepening.

``pvs``
  Principal Variation Search.

``pvscached``
  PVS with transposition table.

``pvsdeep``
  PVS with Iterative Deepening.


All the engines apart from the ``greedy`` one, can be configured with the ``maxdepth``
option. No default value is given. Please, keep in mind that an high ``maxdepth`` requires
more time. Currently the engines are not limited in time.

Alpha-Beta and PVS can change the move ordering algorithm too using the ``ordering``
option that can have the following values:

* ``seq``: Sequential order (follow the order of the move generator).
* ``random``: Random order.
* ``eval``: Sort by board evaluation (slow).
* ``diff``: Sort by board evaluation but just compute the difference of gain
  introduced by the move.

Default value is ``seq``, recommended value is ``diff``.


Passing parameters
~~~~~~~~~~~~~~~~~~

The ``bm`` and ``game`` command have a weird way to pass parameters to the engine.
You can setup the configuration of the engine using the following format::

    engine_name:param1:param2:...

The params are in this order: ``maxwidth``, ``ordering``. (for the engines that support them).


Contributions
-------------

The code is structured to make it easy to plug new algorithms. Actually as it was written
in the spare time you might find useful to refactor some classes. Don't be shy and submit
a pull request!

Some tips on what should be improved:

* Better way to handle counters and information displayed by engines.
* Mixins are quite ugly to plug in. Probably it would be better to have an Engine class
  that is composed by a search algorithm, a cache, an evaluator and a move order strategy.
  Iterative deepening can just wraps a search instead of mix in it.
* Better parameter configuration.
* Tests.
* Time control.
* More algorithms.

This is an overview of the code:


``c4.board``
  The ``Board`` class that represents a connect-four board. Board objects are immutables,
  the ``move`` method creates a new board applying a given move. A `move` is just an
  integer between ``0-7`` (the index of the column).

``c4.evaluate``
  The ``Evaluator`` class implements an heuristic to evaluate a board statically.

``c4.engine``
  All the engines are grouped in this package. Also some utility mixins for the engines
  are here.

``c4.engine.cached``
  ``CachedEngineMixin`` adds a cache (or transposition table) to an the engine.
  It enhance the ``search`` method used by negamax derived engines.

``c4.engine.deepening``
  ``IterativeDeepeningEngineMixin`` plugs iterative deepening to the search by overriding
  the ``choose`` method of a negamax derived engine.

``c4.moveorder``
  Move ordering used by alpha-beta based engines. Move ordering affect the pruning
  massively.

``c4.cache``
  Transposition table implementation.

``c4.game``
  Handle a game between two players.

``c4.arena``
  Handle a tournament between multiple players.

``c4.tables``
  Some precomputed tables.


.. _`zero-sum games`: http://en.wikipedia.org/wiki/Zero%E2%80%93sum_game
.. _`Negamax`: http://en.wikipedia.org/wiki/Negamax
.. _`Alpha beta pruning`: http://en.wikipedia.org/wiki/Alpha-beta_pruning
.. _`Principal variation search`: http://en.wikipedia.org/wiki/Principal_variation_search
.. _`Transposition table`: http://en.wikipedia.org/wiki/Transposition_table
.. _`Iterative deepening`: http://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
