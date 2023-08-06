from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result


class SegmentProfileAction(ActionRunner):

    def __init__(self, *args, **kwargs):
        pass

    async def run(self, payload):
        self.profile.operation.segment = True
        return Result(value={}, port="payload")


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi.process_engine.action.v1.operations.segment_profile_action',
            className='SegmentProfileAction',
            inputs=["payload"],
            outputs=["payload"],
            init=None,
            manual="segment_profiles_action"
        ),
        metadata=MetaData(
            name='Force segmentation',
            desc='Segment profile when flow ends.This action forces segmentation on profile after flow ends. See '
                 'documentation for more information.',
            type='flowNode',
            width=200,
            height=100,
            icon='segment',
            group=["Operations"]
        )
    )
