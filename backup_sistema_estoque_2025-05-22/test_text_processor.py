#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from text_processor import TextProcessor, process_text

class TestTextProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = TextProcessor()
        self.sample_text = """
90 tilápias
16,984
1,84kg bacalhau 
1,476kg Surubim
2,248kg pescada amarela 
4 camarão eviscerado
9 limpo g
21,548kg c promoção
8 eviscerado xg
2 camarão p molho
"""

    def test_normalize_number(self):
        self.assertEqual(self.processor.normalize_number("90"), 90.0)
        self.assertEqual(self.processor.normalize_number("16,984"), 16.984)
        self.assertEqual(self.processor.normalize_number("1,84kg"), 1.84)
        self.assertEqual(self.processor.normalize_number("21.548"), 21.548)
        self.assertEqual(self.processor.normalize_number("1.000,50"), 1000.50)

    def test_identify_product(self):
        # Teste com nomes exatos
        self.assertEqual(self.processor.identify_product("Tilápia"), 1)
        self.assertEqual(self.processor.identify_product("Bacalhau"), 5)
        
        # Teste com variações
        self.assertEqual(self.processor.identify_product("tilápias"), 1)
        self.assertEqual(self.processor.identify_product("limpo g"), 7)
        self.assertEqual(self.processor.identify_product("eviscerado xg"), 10)
        self.assertEqual(self.processor.identify_product("camarão p molho"), 8)
        
        # Teste com texto parcial
        self.assertEqual(self.processor.identify_product("pescada amarela"), 6)
        self.assertEqual(self.processor.identify_product("pescada"), 6)

    def test_parse_line(self):
        # Teste com diferentes formatos de linha
        tilapia = self.processor.parse_line("90 tilápias")
        self.assertEqual(tilapia['produto_id'], 1)
        self.assertEqual(tilapia['quantidade'], 90.0)
        self.assertEqual(tilapia['unidade'], 'un')
        
        bacalhau = self.processor.parse_line("1,84kg bacalhau")
        self.assertEqual(bacalhau['produto_id'], 5)
        self.assertEqual(bacalhau['quantidade'], 1.84)
        self.assertEqual(bacalhau['unidade'], 'kg')
        
        # Teste com promoção
        promocao = self.processor.parse_line("21,548kg c promoção")
        self.assertIsNotNone(promocao)  # Deve identificar algum produto
        self.assertEqual(promocao['quantidade'], 21.548)
        self.assertEqual(promocao['unidade'], 'kg')

    def test_parse_text(self):
        results = self.processor.parse_text(self.sample_text)
        
        # Verificar se todos os itens foram processados
        self.assertEqual(len(results), 10)
        
        # Verificar alguns itens específicos
        self.assertEqual(results[0]['nome'], 'Tilápia')
        self.assertEqual(results[0]['quantidade'], 90.0)
        
        self.assertEqual(results[2]['nome'], 'Bacalhau')
        self.assertEqual(results[2]['quantidade'], 1.84)
        self.assertEqual(results[2]['unidade'], 'kg')
        
        # Verificar se o camarão eviscerado XG foi identificado corretamente
        ev_xg = None
        for item in results:
            if item['nome'] == 'Camarão Eviscerado XG':
                ev_xg = item
                break
        
        self.assertIsNotNone(ev_xg)
        self.assertEqual(ev_xg['quantidade'], 8.0)
        self.assertEqual(ev_xg['unidade'], 'un')

    def test_process_text_function(self):
        # Testar a função de conveniência
        results = process_text(self.sample_text)
        self.assertEqual(len(results), 10)
        
        # Verificar se todos os produtos têm os campos necessários
        for item in results:
            self.assertIn('produto_id', item)
            self.assertIn('nome', item)
            self.assertIn('quantidade', item)
            self.assertIn('unidade', item)


if __name__ == '__main__':
    unittest.main()
