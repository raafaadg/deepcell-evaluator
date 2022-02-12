#!/usr/bin/env python3

from aws_cdk import core

from deepcell_evaluator.pipeline_stack import PipelineStack

app = core.App()

PipelineStack(
    app,
    'DeepcellPipelineStack',
    # env={
    #     'account':'091245778239',
    #     'region': 'us-east-1'}
    )

app.synth()