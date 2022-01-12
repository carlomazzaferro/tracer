from tracer.celery_app import celery_app


# from tracer.api.service.ethereum import EthereumNodeService


@celery_app.task(acks_late=False)
def backfill_blocks(from_block: int, to_block: int):
    """deploy_message.
    Notify about a deployment. We notify if and only if the principal is in the list
    of principals for which we notify.

    Parameters
    ----------
    from_block : str
        starting block
    to_block : str
        ending block
    """
