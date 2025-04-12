import unittest
from valiant_predict_movement import predict_enemy_movement

class TestPredictEnemyMovement(unittest.TestCase):
    def test_predict_enemy_movement(self):
        # Test grid with enemy ship (^) at (6,4) and allied ship (#) at (5,7)
        test_grid = [
            ['a08', 'b08', 'c08', 'd08', 'e08', 'f#8', 'g08', 'h08'],
            ['a07', 'b07', 'c07', 'd07', 'e07', 'f07', 'g07', 'h07'],
            ['a06', 'b06', 'c06', 'd06', 'e$6', 'f06', 'g06', 'h06'],
            ['a05', 'b05', 'c05', 'd05', 'e$5', 'f$5', 'g^5', 'h05'],
            ['a04', 'b04', 'c04', 'd04', 'e04', 'f04', 'g04', 'h04'],
            ['a03', 'b03', 'c03', 'd03', 'e03', 'f03', 'g03', 'h$3'],
            ['a02', 'b02', 'c02', 'd02', 'e$2', 'f02', 'g02', 'h02'],
            ['a01', 'b01', 'c01', 'd01', 'e01', 'f01', 'g01', 'h01']
        ]

        initial_position = (3, 6)  # Position of enemy ship (^)
        expected_next_position = (2, 6)  # Expected movement towards allied ship

        result = predict_enemy_movement(test_grid, initial_position)
        self.assertEqual(result, expected_next_position)

    def test_predict_enemy_movement_1(self):
        # Test grid with enemy ship (^) at (6,4) and allied ship (#) at (5,7)
        # Example usage when run directly

        test_grid = [
            ['a08', 'b08', 'c08', 'd08', 'e08', 'f#8', 'g08', 'h08'],
            ['a07', 'b07', 'c07', 'd07', 'e07', 'f07', 'g07', 'h07'],
            ['a06', 'b06', 'c06', 'd06', 'e$6', 'f06', 'g$6', 'h06'],
            ['a05', 'b05', 'c05', 'd05', 'e$5', 'f05', 'g^5', 'h05'],
            ['a04', 'b04', 'c04', 'd04', 'e04', 'f04', 'g04', 'h04'],
            ['a03', 'b03', 'c03', 'd03', 'e03', 'f03', 'g03', 'h$3'],
            ['a02', 'b02', 'c02', 'd02', 'e$2', 'f02', 'g02', 'h02'],
            ['a01', 'b01', 'c01', 'd01', 'e01', 'f01', 'g01', 'h01']
        ]
        initial_position = (3, 6)  # Position of enemy ship (^)
        expected_next_position = (3, 5)  # Expected movement towards allied ship

        result = predict_enemy_movement(test_grid, initial_position)
        self.assertEqual(result, expected_next_position)

    def test_predict_enemy_movement_3(self):
        # Test grid with enemy ship (^) at (6,4) and allied ship (#) at (5,7)
        # Example usage when run directly

        test_grid = [
            #  0.     1.     2.     3.     4.     5.     6.     7
            ['a08', 'b08', 'c08', 'd08', 'e08', 'f#8', 'g08', 'h08'], # 0
            ['a07', 'b07', 'c07', 'd07', 'e07', 'f07', 'g07', 'h07'], # 1
            ['a06', 'b06', 'c06', 'd06', 'e$6', 'f06', 'g06', 'h06'], # 2
            ['a05', 'b05', 'c05', 'd05', 'e$5', 'f05', 'g^5', 'h05'], # 3
            ['a04', 'b04', 'c04', 'd04', 'e04', 'f04', 'g04', 'h04'], # 4
            ['a03', 'b03', 'c03', 'd03', 'e03', 'f03', 'g03', 'h$3'], # 5
            ['a02', 'b02', 'c02', 'd02', 'e$2', 'f02', 'g02', 'h02'], # 6
            ['a01', 'b01', 'c01', 'd01', 'e01', 'f01', 'g01', 'h01']  # 7
        ]
        initial_position = (3, 6)  # Position of enemy ship (^)
        expected_next_position = (2, 6)  # Expected movement towards allied ship

        result = predict_enemy_movement(test_grid, initial_position)
        self.assertEqual(result, expected_next_position)

if __name__ == '__main__':
    unittest.main()
