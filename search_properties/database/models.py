from dataclasses import dataclass, field
from typing import Optional, Union


@dataclass
class Join:
    join_table: str
    join_column: str
    parent_table: Optional[str] = None
    parent_column: Optional[str] = None
    type_: Optional[str] = None

    def __post_init__(self):
        if not self.join_column:
            self.column1 = "id"
        if not self.parent_column:
            self.column2 = "id"
        if not self.type_:
            self.type_ = 'LEFT'

    def __repr__(self):
        return (
            f"{self.type_} JOIN {self.join_table} on "
            f"{self.join_table}.{self.column1} = "
            f"{self.parent_table}.{self.column2} "
        )


@dataclass
class Query:
    table: Optional[str] = None
    base_query: Optional[str] = None
    columns: Optional[Union[list[str], str]] = None
    where: Optional[dict[str]] = None
    order_by: Optional[list[str]] = None
    joins: Optional[list[Join]] = field(default_factory=list)
    limit: Optional[str] = None

    def __post_init__(self):
        if not self.table and not self.base_query:
            raise ValueError("at least either table or base_query are needed")

        if not self.columns:
            self.columns = "*"
        else:
            self.columns = ",".join(self.columns)

    def get_query(self) -> str:
        repr_ = self.base_query
        if not repr_:
            repr_ = f"SELECT {self.columns} from {self.table} "
            for join in self.joins:
                repr_ += repr(join) + " "

        if self.where:
            filters_query = "AND ".join(
                [f'{key} = "{value}"' for key, value in self.where.items()]
            )
            repr_ += f"WHERE {filters_query} "
        if self.order_by:
            ordering = list(
                map(
                    lambda order: order.replace("-", "") + " DESC"
                    if order.startswith("-")
                    else order,
                    self.order_by,
                )
            )
            repr_ += f'ORDER BY {"".join(ordering)} '
        if self.limit:
            repr_ += f"LIMIT {self.limit}"
        return repr_
