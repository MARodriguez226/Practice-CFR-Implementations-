# Practice-CFR-Implementations-
Implemented the Vanilla CFR algorithm on subgames of poker like Kuhn Poker and Shortest Deck. Additionally, there's a crude implementation of a Heads Up No Limit Hold'em solver.

These games are solved using CFR, a regret-minimizing Nash equilibrium algorithm. The paper used for the implementation of the CFR algorithm was "Regret Minimization in Games with Incomplete Information" [https://martin.zinkevich.org/publications/regretpoker.pdf].

Kuhn Poker is a common toy game of poker invented by Harold W. Kuhn, traditionally used to teach the concept of mixed Nash equilibrium strategies in imperfect information extensive-form games. I used this game as a starting point for CFR implementation and solved for the full game tree without any form of abstraction.

Shortest Deck is a variation of no-limit hold'em where the only cards in play are those excluded in the game of Short Deck [Deck = Deck - Short Deck], and the game only involves 2 streets of action pre-flop and post-flop. I used this bigger game to help tackle problems that may have occurred with increasing my game states. I used suit isomorphisms and betting abstractions to implement a version of this game with a reasonable size. The final game was solved using 1 preflop sizing {300%} and 4 post-flop sizings {33%, 66%, 150%, all-in}.

Heads Up No Limit Texas Hold'em (HUNL) was the last major challenge in my CFR implementations, and improvements remain to be made. The game was abstracted using Waugh's Fast and Optimal Hand Isomorphism Algorithm [https://cdn.aaai.org/ocs/ws/ws0977/7042-30528-1-PB.pdf], which uses rank sets and colex-indexing to create hand suit isomorphisms. In addition, K-means clustering was used to create buckets of flops, turns, and rivers to reduce the game tree into something computationally realistic. We used ideas from Michael Johanson's "Evaluating State-Space Abstractions in Extensive-Form Games" [https://webdocs.cs.ualberta.ca/bowling/papers/13aamas-abstraction.pdf] using the Opponent Hand Strength Clusters (OHSC) metric to determine our clustering. In the interest of time and computation, we additionally used subsets from GTO Wizard's Flop Subset and Abstraction Blog [https://blog.gtowizard.com/poker-subsets-and-abstractions/] as centers to implement K-means++. Due to computational constraints, we were limited to 6 preflop buckets, 3 flop buckets, 3 turn buckets, and 3 river buckets. The game was solved using 1 preflop sizing {300%} and 3 post-flop sizings {33%, 66%, all-in} (various other post-flop sizing combinations were solved as well, which incorporated overbetting). Additionally, Monte Carlo CFR was used in this implementation as only a random subset of cards was used to compute the strategy. In the future, to aid with computational cost, I would like to implement Single Deep CFR [https://www.semanticscholar.org/reader/fd4ca6d2aa21e3b486e1ec38fbf4640853091dc3], a variant of Deep CFR which uses values networks to approximate utility at a given node. This would cut the need to iterate through the entire game tree to find the utility of a certain action and allow for almost no bucketing to be done.

Since the solution.txt files can get pretty large I uploaded a few to this dropbox for people to check out.Just for a quick formatting guide, 
[cards/buckets] [history] [frequencies] 
history = {??: pre-flop, &&: flop , @@: Turn, ##: river, x:check, {p,b,B,O,a}: bet, f:fold}
frequencies, in order of most passive possible move [check/call] to least passive [all-in], when possible last element always fold.
ex. 2s2h 3h4h3c ??pc&&xbB [.60,.10,.30], here we have 2s2h, the pre-flop action when raise-call, the flop came 3h4h3c and opponent checked (x) we bet 33% (b) and opponent raised 75% (B), we are left with 3 possible options [call, all-in, fold], with frequencies call 60%, all-in 10%, and fold 30%.

solution will be posted on a rolling biases:
https://www.dropbox.com/scl/fo/ehkh54xx2ng7zjmgqpkya/h?rlkey=7ly2uuyukkvzxgc1tlbve4ixm&dl=0
