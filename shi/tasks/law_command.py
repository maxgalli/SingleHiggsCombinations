# coding: utf-8

"""
law command:

law run PlotLikelihoodScan  --version hh_bbbb_trylaw  --datacards "datacard_bbbb/datacard.txt" --LikelihoodScan-custom-args='--X-rtd TMCSO_AdaptivePseudoAsimov=0 --X-rtd TMCSO_PseudoAsimov=0    --X-rt MINIMIZER_freezeDisassociatedParams   --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2  --freezeParameters lumiscale --setParameters lumiscale=21.8' --pois kl --scan-parameters kl,-5,10,20 --show-points

"""


import law
import luigi

from dhi.tasks.likelihoods import PlotLikelihoodScan


class bbbbCommands(PlotLikelihoodScan):
    """
    A simple hello world task that extends PlotUpperLimits from DHI.

    This task adds a custom printout before and after running the parent task,
    demonstrating how to extend existing DHI functionality.
    """

    task_namespace = "shi"

    custom_arg = luigi.Parameter(
        default="a string",
        description="a custom custom string to pass to law"
    )


    def __init__(self, *args, **kwargs):
        super(bbbbCommands, self).__init__(*args, **kwargs)

        # Print initialization message
        print("\n" + "=" * 80)
        #print(f"Custom message: {self.arg}")
        print("This should go in law") 
        print("=" * 80 + "\n")

    def requires(self):
        """
        Override requires() to inject `custom_arg` into the inner LikelihoodScan tasks.
        """
        reqs = super(bbbbCommands, self).requires()

        # Sometimes super().requires() returns a list or a single task.
        # Let's normalize to a list of tasks.
        if not isinstance(reqs, (list, tuple)):
            reqs = [reqs]

        # Loop over the first level (usually MergeLikelihoodScan tasks)
        for merge_task in reqs:
            # Make sure the merge task has a requires() method
            if not hasattr(merge_task, "requires"):
                continue

            # Call requires() to get its dependencies (the LikelihoodScan tasks)
            sub_reqs = merge_task.requires()
            if isinstance(sub_reqs, dict):
                sub_tasks = sub_reqs.values()
            elif isinstance(sub_reqs, (list, tuple)):
                sub_tasks = sub_reqs
            else:
                sub_tasks = [sub_reqs]

            # Now inject custom_arg into all LikelihoodScan tasks we find
            for sub_task in sub_tasks:
                if hasattr(sub_task, "LikelihoodScan-custom-args"):
                    sub_task.LikelihoodScan_custom_args = self.custom_arg
                elif hasattr(sub_task, "custom_args"):
                    sub_task.custom_args = self.custom_arg
                    #sub_task.combine_optimization_args = ""
                else:
                    print(f"[WARN] Could not inject into {sub_task.__class__.__name__}")

        return reqs
        
    @law.decorator.log
    @law.decorator.notify
    def run(self):
        """
        Extended run method with custom printouts.
        """
        # Custom printout before running parent task
        self.publish_message("\n" + "=" * 80)
        self.publish_message(f">>> {self.custom_arg}")
        self.publish_message(">>> Starting to create upper limit plot using DHI task...")
        self.publish_message(">>> Task parameters:")
        self.publish_message(f"    - POIs: {self.pois}")
        self.publish_message(f"    - Datacards: {len(self.datacards)} file(s)")
        self.publish_message(f"    - Scan parameters: {self.scan_parameters}")
        self.publish_message(f"    - Version: {self.version}")
        self.publish_message("=" * 80 + "\n")

        #add custom args
        self.LikelihoodScan_custom_args = self.custom_arg
        
        # Run the parent task (PlotUpperLimits)
        result = super(bbbbCommands, self).run()

        # Custom printout after running parent task
        self.publish_message("\n" + "=" * 80)
        self.publish_message(">>> DHI task completed successfully!")

        # Handle output (can be dict or single target)
        output = self.output()
        if isinstance(output, dict):
            self.publish_message(">>> Outputs:")
            for key, target in output.items():
                if isinstance(target, list):
                    self.publish_message(f"    - {key}:")
                    for t in target:
                        self.publish_message(f"        {t.path}")
                else:
                    self.publish_message(f"    - {key}: {target.path}")
        else:
            self.publish_message(f">>> Output: {output.path}")

        self.publish_message(">>> SHI HelloWorld task finished!")
        self.publish_message("=" * 80 + "\n")

        return result
