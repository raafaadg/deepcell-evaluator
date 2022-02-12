from aws_cdk.core import Stage, Construct

from deepcell_evaluator.deepcell_evaluator_stack import DeepcellEvaluatorStack
from deepcell_evaluator.site_stack import DeepcellPublicSiteS3

class WebServiceStage(Stage):
  def __init__(self, scope: Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)
    
    props = {}
    props['namespace'] = self.node.try_get_context('namespace')
    props['domain_name'] = self.node.try_get_context('domain_name')    
    
    DeepcellEvaluatorStack(self, 'Deepcell-Resources-WebService')
    
    DeepcellPublicSiteS3(
        self,
        f'{props["namespace"]}-PublicSite-WebService',
        site_domain_name=props["domain_name"]
    )    