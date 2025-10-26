import attr 



@attr.s(frozen=True, order=True, slots=True)
class Comment:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    text: str = attr.ib(default="", converter=str)
    replies: list[int] = attr.ib(factory=list, repr=False, cmp=False, hash=False)


def main () -> None:
    comment: Comment = Comment(1, "I Just subscribed!")
    print(f'{comment = }')
    # print(f'{attr.as_tuple(comment) = }')
    # print(f'{attr.as_dict(comment) = }')
    # comment.id = 2  # will raise error because of frozen=True         
    print(f'{attr.fields(Comment) = }')
    print(attr.fields_dict(Comment))
  #gathrEx  print(attr.validators.validate(comment))
    print(attr.evolve(comment, text="New Text"))
    print(f'{comment = }')

if __name__ == "__main__":
    main()
