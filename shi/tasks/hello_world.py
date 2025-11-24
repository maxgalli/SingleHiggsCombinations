# coding: utf-8

"""
Hello World example task that extends CWF tasks.

This demonstrates how to import and extend tasks from the combine_workflow repository.
"""

import law
import luigi

from cwf.tasks.base import AnalysisTask


class HelloWorld(AnalysisTask):
    """
    A simple hello world task that extends AnalysisTask from CWF.

    This task demonstrates how to create custom tasks that work with the
    combine_workflow infrastructure.
    """

    task_namespace = "shi"

    custom_message = luigi.Parameter(
        default="Hello from Single Higgs Combinations!",
        description="a custom message to print; default: 'Hello from Single Higgs Combinations!'",
    )

    datacard = luigi.Parameter(
        default="",
        description="path to a datacard file (optional); default: ''",
    )

    def __init__(self, *args, **kwargs):
        super(HelloWorld, self).__init__(*args, **kwargs)

        # Print initialization message
        print("\n" + "=" * 80)
        print("SHI HelloWorld Task Initialized!")
        print(f"Custom message: {self.custom_message}")
        print("This task extends: cwf.tasks.base.AnalysisTask")
        print("=" * 80 + "\n")

    def output(self):
        """
        Define the output target for this task.
        """
        return self.local_target("hello_world_output.txt")

    @law.decorator.log
    def run(self):
        """
        Run the hello world task.
        """
        # Print task information
        print("\n" + "=" * 80)
        print(f">>> {self.custom_message}")
        print(">>> Running SHI HelloWorld task...")
        print(">>> Task parameters:")
        print(f"    - Version: {self.version}")
        if self.datacard:
            print(f"    - Datacard: {self.datacard}")
        print("=" * 80 + "\n")

        # Create output
        output = self.output()
        output.parent.touch()

        # Write some content to the output file
        with output.open("w") as f:
            f.write(f"{self.custom_message}\n")
            f.write(f"Task version: {self.version}\n")
            if self.datacard:
                f.write(f"Datacard: {self.datacard}\n")
            f.write("\nThis is a simple example task that extends CWF AnalysisTask.\n")
            f.write("You can use this as a template for creating more complex tasks.\n")

        # Print completion message
        print("\n" + "=" * 80)
        print(">>> SHI HelloWorld task completed successfully!")
        print(f">>> Output: {output.path}")
        print("=" * 80 + "\n")
