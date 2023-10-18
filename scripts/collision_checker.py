class CollisionChecker:
    colliders = []
    
    @classmethod 
    def add_collider(cls, collider) -> bool:
        cls.colliders.append(collider)
    
    @classmethod 
    def clear_colliders(cls) -> None:
        cls.colliders = []

    @classmethod
    def check_collisions(cls, collider) -> bool:
        for other in cls.colliders:
            if other.colliderect(collider) and other != collider:
                return True
        
        return False