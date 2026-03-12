from fastapi import HTTPException


def raise_not_found(resource: str, id: int):
    raise HTTPException(
        status_code=404,
        detail={
            "code": "NOT_FOUND",
            "message": f"{resource} with id {id} not found",
            "field": None,
        },
    )


def raise_duplicate(field: str, value: str):
    raise HTTPException(
        status_code=409,
        detail={
            "code": "DUPLICATE",
            "message": f"A record with {field} '{value}' already exists",
            "field": field,
        },
    )


def raise_forbidden(message: str = "You do not have permission to perform this action"):
    raise HTTPException(
        status_code=403,
        detail={
            "code": "FORBIDDEN",
            "message": message,
            "field": None,
        },
    )


def raise_unauthorized(message: str = "Authentication required"):
    raise HTTPException(
        status_code=401,
        detail={
            "code": "UNAUTHORIZED",
            "message": message,
            "field": None,
        },
    )


def raise_bad_request(message: str, field: str = None):
    raise HTTPException(
        status_code=400,
        detail={
            "code": "BAD_REQUEST",
            "message": message,
            "field": field,
        },
    )