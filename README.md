# Phrase Generator — Anki Add-on (v0.1)

First prototype of a phrase-generation add-on for language learning.

## What it does

The add-on provides an HTML form inside Anki and composes a structured prompt from the user's choices.

Current user-configurable fields:

- Generate by: word / term / chunk / grammar rule
- Grammar rule / target
- Amount of phrases
- Subjects / context
- Phrase size: S / M / L
- Examples
- Blacklist

The following are internal rules and are always included in the prompt:

- Balance pronouns
- Balance affirmative / negative / interrogative forms
- Use the application's Anki card output format
- Prefer natural, useful English

## Current limitation

This version does NOT call an AI API.

It only composes the prompt and shows it in the add-on window. The prompt can be copied and sent manually to an AI.

## Installation

1. Extract the `phrase_generator` folder into Anki's `addons21` directory.
2. Restart Anki.
3. Open `Tools -> Phrase Generator`.

The add-on currently targets Anki installations that provide Qt WebEngine and Qt WebChannel.

## Next planned layer

A future version can replace the manual copy step with an AI provider interface:

HTML Form
-> GenerationConfig
-> PromptBuilder
-> AI Provider
-> Generated phrases
-> Anki card parser
-> Anki notes/cards
