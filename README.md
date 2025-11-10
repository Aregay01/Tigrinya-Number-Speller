# Number Speller — Tigrinya Number-to-Text Converter

A robust, well-documented Python implementation that converts numeric values into their Tigrinya spelled-out form.  
This project preserves the original procedural logic while reorganizing it into a maintainable class (`NumberSpeller`), adding defensive checks, and commenting every line for easier understanding and extension.

---

## Table of contents

- [Features](#features)
- [Language / Locale](#language--locale)
- [Installation](#installation)
- [Usage](#usage)
  - [Simple example](#simple-example)
  - [API / Methods](#api--methods)
- [Behavior notes & design choices](#behavior-notes--design-choices)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- Converts integers and floating-point numbers to their spelled-out representation in **Tigrinya**.
- Preserves the exact logic of the original script (including the sanitiser and recursive integer spelling).
- Class-based API (`NumberSpeller.spell(n)`) to make reuse and testing straightforward.
- Defensive input handling (numeric coercion, clear error messages).
- Every line in the code includes a comment explaining what it does — ideal for learning or porting.
- Handles negative numbers and fractional parts (decimal point + each fractional digit spelled separately).
- Designed to be easy to extend (add more large-scale number names, localization, formatting options).

---

## Language / Locale

- Output language: **Tigrinya** (Ethiopia / Eritrea script)
- This implementation encodes Tigrinya number words directly in the code (UTF-8). The repository assumes UTF-8 in source files.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/number-speller-tigrinya.git
cd number-speller-tigrinya
