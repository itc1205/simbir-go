from fastapi import APIRouter, Depends
from simbir_go_backend.entrypoint.dependencies.uow import get_uow
from simbir_go_backend.entrypoint.dependencies.auth import get_current_account

from simbir_go_backend.entrypoint.exceptions import NotEnoughPrivileges

from simbir_go_backend.service.account_services import HESOYAM

router = APIRouter(prefix="/Payment", tags=["PaymentController"])

@router.post("/{id:int}")
def hesoyam(id: int, user=Depends(get_current_account), uow=Depends(get_uow)):
    if user.id != id and not user.isAdmin:
        raise NotEnoughPrivileges
    HESOYAM(id, uow)
    return 200