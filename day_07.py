r"""
--- Day 7: The Sum of Its Parts ---

You find yourself standing on a snow-covered coastline; apparently, you landed a little off course. The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack something that washed ashore. It's quite cold out, so you decide to risk creating a paradox by asking them for directions.

"Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the device on your wrist also be a translator? "Those clothes don't look very warm; take this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have higher priorities at the moment. You see, believe it or not, this box contains something that will solve all of Santa's transportation problems - at least, that's what it looks like from the pictures in the instructions." It doesn't seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input). Each step is designated by a single letter. For example, suppose you have the following instructions:

Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.

Visually, these requirements look like this:


  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----

Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

    Only C is available, and so it is done first.
    Next, both A and F are available. A is first alphabetically, so it is done next.
    Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
    After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
    F is the only choice, so it is done next.
    Finally, E is completed.

So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?

Your puzzle answer was CFMNLOAHRKPTWBJSYZVGUQXIDE.
--- Part Two ---

As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together." Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workers should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds). Then, using the same instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .        
   1        C          .        
   2        C          .        
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE

Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second. Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers can begin multiple steps simultaneously.

In this example, it would take 15 seconds for two workers to complete these steps.

With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?

Your puzzle answer was 971.
"""

from collections import defaultdict
from string import ascii_uppercase
from typing import List, Tuple, Dict, Sequence

with open('day_07.input', 'r') as f:
    data = f.read()

# data = """Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin."""

pairs: List[Tuple[str, str]] = [(line.split()[1], line.split()[7]) for line in data.split('\n')]
pairs = sorted(pairs, key=lambda x: (sum(x[0] == pair[1] for pair in pairs), x))

def topo_sort_pairs(pairs: Sequence[Tuple[str, str]]) -> str:
    """
    Topological sorting of the given pairs, as long as they form a DAG

    First we create the graph, by mapping each vertex to its connected vertices.
    We also store off the degree value for each vertex, this tracks the number of incoming connections.

    We then find all vertices with a 0 degree, and add them to the queue to be processed.
    Then we remove an item from the queue, and walk to each of its connected vertices, removing 1 degree
    as we visit the node.
    If the degree drops to 0, we enqueue that vertex.
    
    Arguments:
        pairs {Sequence[Tuple[str, str]]} -- The graph edges as a pair of nodes.
    
    Returns:
        str -- The graph in sorted order.
    """

    graph: Dict[str, list] = defaultdict(list)
    degrees: Dict[str, int] = defaultdict(int)

    queue: List[str] = []
    processed: List[str] = []

    for u, v in pairs:
        graph[u].append(v)
        degrees[v] += 1

    for u, vs in graph.items():
        vs.sort()
        if not degrees[u]:
            queue.append(u)

    # Reverse sort the queue so the first node alphabetically is always at the end.
    # This way queue.pop() always returns the next node to be processed.
    queue.sort(reverse=True)

    while queue:
        u = queue.pop()
        processed.append(u)
        for v in graph[u]:
            degrees[v] -= 1
            if not degrees[v]:
                queue.append(v)
        queue.sort(reverse=True)
    return ''.join(processed)


def calculate_build_time(pairs: Sequence[Tuple[str, str]], num_workers: int = 5, time_penalty: int = 60) -> int:
    """
    Similar to the above tological sort, except this time we are weighting the nodes based on how long it takes to finish the work
    instead of just their position alphabetically.

    In addition the number of workers is limited, so we've setup a pool of workers where each node is added along with its completion time.
    Nodes are then removed from the pool starting with the fastest built, and the current build time is updated to reflect this new time.
    We then continue traversing the graph, adding items to the work queue until either we run out of items, or fill the pool.
    
    Arguments:
        pairs {Sequence[Tuple[str, str]]} -- The graph edges as a piar of nodes
    
    Keyword Arguments:
        num_workers {int} -- Size of the worker pool (default: {5})
        time_penalty {int} -- Base time it takes to complete each action (default: {60})
    
    Returns:
        int -- Time it takes to complete the job, in seconds.
    """

    def update_pools(queue: List[str], workers: List[Tuple[int, str]]):
        # Probably faster to just have this mutate the pools in place, but I don't like functions that do that.
        queue = queue[:]
        workers = workers[:]
        queue.sort(reverse=True)
        while len(workers) < num_workers and queue:
            u = queue.pop()
            w = (build_time + time_penalty + ascii_uppercase.index(u), u)
            workers.append(w)
        # Reverse sorting the workers, for similar reasons that we reverse sort the queue.
        # This will always remove the node with the lowest build time
        workers.sort(reverse=True)
        return queue, workers

    build_time = 0
    time_penalty += 1
    graph: Dict[str, list] = defaultdict(list)
    degrees: Dict[str, int] = defaultdict(int)

    queue: List[str] = []
    workers: List[Tuple[int, str]] = []

    for u, v in pairs:
        graph[u].append(v)
        degrees[v] += 1

    for u, vs in graph.items():
        vs.sort()
        if not degrees[u]:
            queue.append(u)

    # Spinning up the worker pool, each element in the worker pool is a tuple (time_to_finish: int, node: str)
    # We update the build_time each time we remove an element from the worker pool.
    queue, workers = update_pools(queue, workers)
    while queue or workers:
        build_time, u = workers.pop()
        for v in graph[u]:
            degrees[v] -= 1
            if not degrees[v]:
                queue.append(v)
    
        queue, workers = update_pools(queue, workers)
    return build_time


if __name__ == '__main__':
    print(topo_sort_pairs(pairs[:]))
    print(calculate_build_time(pairs[:])) #, num_workers=2, time_penalty=0))
