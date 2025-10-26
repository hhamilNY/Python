from dataclasses import dataclass, astuple, asdict, field
import dataclasses
from inspect import isfunction, getmembers
import pprint



@dataclass(frozen=True, order=True)
class Comment:
    id: int = field()
    text: str = field(default="")
    replies: list[int] = dataclasses.field(default_factory=list, compare=False, hash=False, repr=False)




def main () -> None:
    comment: Comment = Comment(1, "I Just subscribed!")
    print(f'{comment = }')
    print(f'{astuple(comment) = }')
    print(f'{asdict(comment) = }')
    # comment.id = 2  # will raise error because of frozen=True

    pprint.pprint(getmembers(Comment, isfunction))

    print(dataclasses.replace(comment, text="New Text"))
    print(f'{comment = }')




if __name__ == "__main__":
    main()

