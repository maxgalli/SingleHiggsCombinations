# Single Higgs Combinations (SHI)

Custom tasks for Single Higgs combinations, extending the [Combine Workflow](https://gitlab.cern.ch/cms-analysis/general/combine_workflow).

## Overview

This repository uses the Combine Workflow (CWF) as a foundation and adds custom tasks for Single Higgs analysis combinations. It maintains all the CWF infrastructure while allowing customization of:

- **Combine version**: Uses v10.0.0 (configurable)
- **Custom tasks**: Extends CWF tasks with additional functionality
- **Analysis-specific workflows**: Tailored for Single Higgs combinations

## Repository Structure

```
SingleHiggsCombinations/
├── combine_workflow/       # Combine Workflow tools (submodule)
│   ├── cwf/               # CWF tasks and utilities
│   ├── modules/           # law and plotlib submodules
│   └── setup.sh           # CWF setup script
├── shi/                   # Single Higgs Combinations package
│   ├── __init__.py
│   └── tasks/             # Custom SHI tasks
│       ├── __init__.py
│       └── hello_world.py # Example task extending CWF
├── bin/                   # Custom scripts (optional)
├── .setups/               # Setup configurations
├── setup.sh               # Main setup script (wraps combine_workflow/setup.sh)
├── law.cfg                # Law configuration (extends combine_workflow/law.cfg)
└── README.md              # This file
```

## First-Time Setup

### 1. Clone the Repository

```bash
git clone --recursive <repository-url> SingleHiggsCombinations
cd SingleHiggsCombinations
```

The `--recursive` flag automatically initializes and clones all submodules (including combine_workflow).

### 2. Source the Setup Script

```bash
source setup.sh
```

On first run, this will:
- Install Combine v10.0.0 and CMSSW_11_3_4
- Install the CWF software stack
- Initialize the law and plotlib submodules
- Prompt you for configuration (default setup name: `shi_default`)

**Important**: The setup process may take 15-30 minutes on first run due to CMSSW compilation.

### 3. Index Law Tasks

```bash
law index --verbose
```

This makes law aware of both CWF and SHI tasks for command-line autocompletion.

## Configuration

During the first setup, you'll be prompted for:
- `CWF_USER`: Your CERN/WLCG username
- `CWF_DATA`: Local data directory (default: `./data`)
- `CWF_STORE`: Output store directory
- `CWF_SOFTWARE`: Software installation directory
- And other configuration options

These settings are saved to `.setups/shi_default.sh` for future use.

## Subsequent Usage

After the first setup, simply source the setup script:

```bash
cd SingleHiggsCombinations
source setup.sh
```

This will use your saved configuration from `.setups/shi_default.sh`.

## Combine Version Configuration

### Using Custom Combine Version

By default, this repository uses **Combine v10.0.0** with **CMSSW_11_3_4**. To use a different version:

```bash
CWF_COMBINE_VERSION=v9.0.0 source setup.sh
```

### Reinstalling Combine

To reinstall Combine from scratch:

```bash
CWF_REINSTALL_COMBINE=1 source setup.sh
```

## Available Tasks

### CWF Tasks

All tasks from the Combine Workflow are available:

```bash
law run --help                    # List all tasks
```

See the [Combine Workflow documentation](https://gitlab.cern.ch/cms-analysis/general/combine_workflow) for details.

### SHI Tasks

Custom tasks in the `shi.tasks` namespace:

```bash
law run shi.HelloWorld --help     # Example task extending CWF
```

## Example: Hello World Task

The `HelloWorld` task demonstrates how to extend CWF tasks:

```bash
law run shi.HelloWorld \
    --version dev \
    --custom-message "My custom analysis!" \
    --datacard path/to/datacard.txt
```

This task:
- Extends `cwf.tasks.base.AnalysisTask`
- Adds custom printouts and parameters
- Creates a simple output file demonstrating the workflow

## Creating New SHI Tasks

To create a new custom task:

1. **Create a new file** in `shi/tasks/`:

```python
# shi/tasks/my_task.py
import law
import luigi
from cwf.tasks.base import AnalysisTask

class MyTask(AnalysisTask):
    task_namespace = "shi"

    my_param = luigi.Parameter(
        default="default_value",
        description="my custom parameter"
    )

    def output(self):
        return self.local_target("my_output.txt")

    def run(self):
        # Your custom logic
        output = self.output()
        output.parent.touch()
        with output.open("w") as f:
            f.write(f"Task output: {self.my_param}\n")
```

2. **Add to `shi/tasks/__init__.py`**:

```python
__all__ = [
    "HelloWorld",
    "MyTask",  # Add your task
]

from shi.tasks.hello_world import HelloWorld
from shi.tasks.my_task import MyTask  # Import it
```

3. **Re-index**:

```bash
law index --verbose
```

4. **Run your task**:

```bash
law run shi.MyTask --version dev --help
```

## Updating the Combine Workflow Submodule

To update to a newer version of combine_workflow:

```bash
cd combine_workflow
git fetch origin
git checkout master  # or specific tag/commit
git pull
cd ..
git add combine_workflow
git commit -m "Update combine_workflow submodule"
```

## Environment Variables

Key environment variables set by the setup:

- `SHI_BASE`: Base directory of this repository
- `CWF_BASE`: Base directory of combine_workflow submodule
- `CWF_COMBINE_VERSION`: Combine version (default: v10.0.0)
- `CWF_CMSSW_VERSION`: CMSSW version (default: CMSSW_11_3_4)
- `CWF_DATA`: Data directory
- `CWF_STORE`: Output store directory
- `CWF_SOFTWARE`: Software installation directory

## Troubleshooting

### "combine_workflow/setup.sh not found"

Make sure the combine_workflow submodule is initialized:

```bash
git submodule update --init --recursive
```

### Combine installation fails

Try reinstalling:

```bash
CWF_REINSTALL_COMBINE=1 source setup.sh
```

### Law can't find SHI tasks

Re-index:

```bash
law index --verbose
```

### Setup configuration questions every time

Make sure you're using the same setup name:

```bash
source setup.sh shi_default
```

## Documentation

- [Combine Workflow](https://gitlab.cern.ch/cms-analysis/general/combine_workflow)
- [Law Framework](https://law.readthedocs.io/)
- [Combine Tool](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/)

## Contact

For questions about this repository, contact Massimiliano Galli.

For questions about the Combine Workflow, see the [combine_workflow repository](https://gitlab.cern.ch/cms-analysis/general/combine_workflow).
