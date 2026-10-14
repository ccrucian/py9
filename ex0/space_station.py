from pydantic import Field, BaseModel


class SpaceStation(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    crew_size: int = Field(ge=1, le=20)
    is_operational: bool = True


station = SpaceStation(
    name="ISS",
    #type coercion(automaticconversionoftypes)
    crew_size="6",
    is_operational=True
)


def main() -> None:
    station = SpaceStation(
    name="ISS",
    #type coercion(automaticconversionoftypes)
    crew_size="6",
    is_operational=True
    )
    print(station)


if __name__ == "__main__":
    main()