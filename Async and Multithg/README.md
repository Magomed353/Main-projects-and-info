# Asynchronous Programming and Multiprocessing in Python

A pet project consisting of two console applications: an exam simulator and an image downloader. The project provides hands-on practice with multiple processes, asynchronous tasks, shared data, and network requests.

## Technologies

- **Python 3**
- **multiprocessing** — concurrent examiner processes, shared data through `Manager`, and synchronization through `Lock`.
- **asyncio** — asynchronous download tasks.
- **aiohttp** — HTTP requests.
- **PrettyTable** — console tables for displaying results.

## 1. Exam Simulator

The application simulates an exam with a shared student queue and multiple examiners. Each examiner runs in a separate process.

### Features

- Loading students, examiners, and questions from text files.
- Selecting three random questions for each student.
- Probabilistic answer selection based on the golden ratio.
- Taking the examiner’s mood into account when determining the result.
- Simulating exam durations and lunch breaks.
- Updating console tables with student statuses and examiner statistics.
- Generating a final report.

Once the exam is complete, the application displays student results, examiner statistics, total duration, the best students and examiners, the most successfully answered questions, and the overall outcome.

## 2. Image Downloader

The application accepts image URLs through the console and saves images to the specified location. Downloads use `asyncio` tasks and the `aiohttp` HTTP client.

### Features

- Accepting a save path and checking its existence and write permissions.
- Accepting multiple URLs one at a time.
- Creating image download tasks.
- Determining file extensions from the `Content-Type` header.
- Generating random filenames when saving to a directory.
- Waiting for the created tasks after input is complete.
- Displaying a table of URLs with the statuses of preliminary HTTP requests.

## Project Structure

```text
src/
├── exercise1/
│   ├── task_1.py
│   ├── examiners.txt
│   ├── students.txt
│   └── questions.txt
└── exercise2/
    └── task_2.py
```

## Installation

Python 3 and `pip` are required.

Install the dependencies from the project root:

```bash
python -m pip install aiohttp prettytable
```

## Running the Exam Simulator

Run the application from `src/exercise1`: it looks for input files in the current working directory.

```bash
cd src/exercise1
python task_1.py
```

### Input Data

All files must use UTF-8 encoding.

Each line in `examiners.txt` and `students.txt` contains a name and a gender marker: `М` for male or `Ж` for female. These are Cyrillic characters.

Example `examiners.txt`:

```text
Степан М
Дарья Ж
Михаил М
```

Example `students.txt`:

```text
Петр М
Сергей М
Варвара Ж
```

Each question in `questions.txt` must appear on a separate line. At least three questions are required.

```text
Там стоит стол
Человек собаке друг
Солнечные затмения влияют на людей
Программирование интересное занятие
```

Results may differ between runs because questions, answers, and examiner moods are selected randomly.

## Running the Image Downloader

Run the following commands from the project root:

```bash
mkdir images
python src/exercise2/task_2.py
```

1. Enter an existing directory for saving images, such as `./images`.
2. Enter image URLs one at a time.
3. Submit an empty line to finish entering URLs.
4. Wait for the tasks to complete and the results table to appear.

### Current Limitations

The standard console `input()` call can pause asynchronous tasks while waiting for user input. Network and file-writing errors may currently interrupt the application.

The “Success” status reflects the server’s response to a preliminary request and does not guarantee that the file has been saved.

## Skills Practiced

- Distributing work across multiple processes.
- Synchronizing access to shared data.
- Creating and awaiting asynchronous tasks.
- Working with HTTP requests and the file system.
- Probabilistic modeling.
- Organizing code with classes and functions.
- Building console interfaces and generating summary reports.
