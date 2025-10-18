# Build instructions for Windows

## Requirements:
- Visual Studio 2022
- cmake (>=3.20)
- python (>= 3.10)
- git

## Clone source code.
```cmd
git clone https://github.com/A1ex3/QtProjectTemplate.git
```

### Prepare dependencies. Run "x64 Native Tools Command Prompt for VS 2022" as administrator.
```cmd
python configure.py --drive-letter <DRIVE_LETTER>
```

### Build the project.
```cmd
cmake -B out -A x64 .
```

```cmd
cmake --build out --config <Debug|Release>
```
