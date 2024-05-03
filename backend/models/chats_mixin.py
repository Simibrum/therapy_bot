"""Mixins for the Chats model."""
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, declared_attr, relationship

from models.chats import ChatReferenceAssociation


class HasChatReferences:
    @declared_attr
    def chat_reference_association_id(cls):
        return Column(Integer, ForeignKey("chat_reference_association.id"))

    @declared_attr
    def chat_reference_association(cls):
        name = cls.__name__
        discriminator = name.lower()

        assoc_cls = type(
            f"{name}ChatReferenceAssociation",
            (ChatReferenceAssociation,),
            {
                "__tablename__": None,
                "__mapper_args__": {"polymorphic_identity": discriminator},
            },
        )

        cls.chat_references = association_proxy(
            "chat_reference_association",
            "chat_references",
            creator=lambda chat_references: assoc_cls(chat_references=chat_references),
        )
        return relationship(assoc_cls, backref=backref("parent", uselist=False))
