from typing import Self
from collections import defaultdict, deque
from itertools import product
from more_itertools import ilen


class Area:
    
    directions = [1,-1j,-1,1j]
    plots:set[complex]
    
    def __init__(self, plots:set[complex]) -> None:
        self.plots = plots
    
    def area(self) -> int:
        """Return number of plots in area."""
        return len(self.plots)
    
    def circumference(self) -> int:
        """Count number of plots that have a neighbor not in the area."""
        return ilen(p for p,d in product(self.plots, Area.directions) if p+d not in self.plots)
    
    def sides(self) -> int:
        """For each direction, find all plots that are on the edge towards that
        direction. Within this set find the number of connected components."""
        return sum(len(find_connected_plots({p for p in self.plots if p+d not in self.plots})) for d in Area.directions)


def find_connected_plots(plots:set[complex]) -> list[Area]:
    """Return all individually 4-connected Areas of plots"""
    areas:list[Area] = []
    found:set[complex] = set()
    for position in plots:
        if position in found:
            continue
        area:set[complex] = set()
        queue:deque[complex] = deque([position])
        while queue:
            position = queue.popleft()
            if position in found:
                continue
            area.add(position)
            found.add(position)
            for direction in Area.directions:
                position_ = position+direction
                if position_ in plots:
                    queue.append(position_)
        areas.append(Area(area))
    return areas


def parse_input(file_handle) -> list[Area]:
    """For each type of plant, find the set of plots that have the type. Then
    find all 4-connected components per set of different plant types."""
    plant_type_per_plot:dict[complex,str] = {}
    plots_per_plant_type:defaultdict[str,set[complex]] = defaultdict(set)
    for r,row in enumerate(l.strip() for l in file_handle.readlines()):
        for c,plot in enumerate(row):
            plant_type_per_plot[c+r*1j] = plot
            plots_per_plant_type[plot].add(c+r*1j)
    return [a for s in plots_per_plant_type.values() for a in find_connected_plots(s)]


def part1(problem_input:list[Area]) -> int:
    return sum(area.area()*area.circumference() for area in problem_input)


def part2(problem_input:list[Area]) -> int:
    return sum(area.area()*area.sides() for area in problem_input)
