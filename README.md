# AcademicArmy

AcademicArmy is a multi-agent system for producing research papers. Its core idea is to separate ideation, blueprinting, writing, coding, testing, optimization, visualization, and review into specialized roles that work from a shared paper blueprint.

## How To Use

Start with an idea. The idea can be rough or detailed; it does not need to be a complete research plan.

Give the idea to `ProductManager`. ProductManager understands the AcademicArmy workflow and helps organize the idea into a paper blueprint, also called the construction plan. Because an early idea is usually underspecified, ProductManager should interact with you over multiple rounds to converge the blueprint toward what you actually want.

Once you are satisfied with the paper blueprint, the formal AcademicArmy workflow begins. The blueprint becomes the project starting point for writing the paper, implementing experiments, running tests, optimizing code, drawing illustrations, plotting results, and reviewing the manuscript.

## Guiding Principle

The central principle of AcademicArmy is: build according to the blueprint.

The blueprint produced by ProductManager should be specific enough for each role to start working without needing to redesign the project. AcademicArmy then follows that standardized plan to complete the paper and its supporting artifacts.

## Project Structure

See `AcademicArmy/README.md` for the agent and team structure.
