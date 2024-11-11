from source.Interpretator import StarIntepretator
import sys

interpretator = StarIntepretator(sys.argv)
std = StarIntepretator([0, "runtime/__init__.star"])
std.run()

interpretator.preload_memory(std.get_memory())
interpretator.run()



