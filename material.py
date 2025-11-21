class Material():
    def __init__(self, reflective=0, transparent=0, emitive=0, refractive_index=1):
        self.reflective = reflective        # 0-1
        self.transparent = transparent      # 0-1
        self.emitive = emitive              # 0-1
        self.refractive_index = refractive_index
