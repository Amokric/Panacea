## Synopsis

Pancea is a framework to build multi-agent systems in Python. It allows developers to easily define their model's environment, create different types of agents each with their own 
set of rules and observe them evolve and interact with the environment. The framework is particularly suited for problems involving modelling and simulation of natural systems.

Current Version (22/05/2016): ALPHA 1

## Motivation
Complex systems are a fascinating area of study. Just looking at the natural world, we can see how some extremely complex
behaviours exhibited by groups of organisms do not appear to be coordinated or controlled by any central entity. These are
known as emergent properties of the groups, where the behaviour of single members dictated by relatively simple rules gives
rise to overall group behaviours more complex than any individual could coordinate.

Examples of emergent behaviours include bird flocking, the movements of schools of fish, light emission in bioluminescent
plancton and immune responses in humans. Moving away from biology, we find emergent behaviours in chemical reactions
(Eg: Redox), sociology (Eg: Migration), finance (Eg: The Stock Market) and generally speaking any sufficiently complex
system comprising of multiple independent agents.

Understanding such systems can allow us to obtain a better understanding of their dynamics and nature. For example,
in the field of medicine, understanding the dynamics behind cancer growth and expansion can allow us to devise better, more
efficient treatments. Similarly, in biology, understanding which conditions favour or inhibit proliferation of micro-organisms
can be a valuable asset in research.

An alternative to wetware (laboratory/real world) solutions is offered by in-silico investigations. This approach proposes to
create a virtual model of the system we are interested in allowing to simulate its evolution under various conditions and to
collect useful results.

While multi-agent systems have already been studied, these often were implemented using ad-hoc solutions. That is, the
software that was used to build and simulate such models was written expressly for such task and might have not suited
another type of model.

Panacea wants to be a general-purpose multi-agent framework suited to implementing models studying any system or behaviour. It wishes to offer easy access to relevant tools which will allow to easily and rapidly deploy efficient simulations.
In addition, Panacea also wants to promote experimental reproducibility. It does this by encouraging users to define their experimental starting conditions using our own XML data structure, allowing experiments to be then validated by other
users with the certainty of the setup being identical.

## Installation

Simply import the /core directory into your workspace.


## Tests

All tests are contained in /tests.

## Contributors

Dario Panada


MRes in Advanced Computer Science Candidate

The University of Manchester (UK)

dario.panada@postgrad.manchester.ac.uk

## License

The MIT License (MIT)
Copyright (c) 2016 Dario Panada

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.