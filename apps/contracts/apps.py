from django.apps import AppConfig


class ContractsConfig(AppConfig):
    name = 'contracts'
    verbose_name = "合同管理"

    def ready(self):
        import contracts.signals
