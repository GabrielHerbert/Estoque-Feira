#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sqlite3
from typing import List, Dict, Any, Tuple, Optional
from rapidfuzz import process, fuzz

class TextProcessor:
    def __init__(self, db_path: str = 'estoque.db'):
        """
        Inicializa o processador de texto com a conexão ao banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados SQLite
        """
        self.db_path = db_path
        self.produtos = self._load_produtos()
        self.produto_map = {p['id']: p for p in self.produtos}
        self.produto_nomes = [p['nome'].lower() for p in self.produtos]
        
        # Dicionário de variações de nomes de produtos
        self.variacoes = {
            'tilápia': ['tilapia', 'tilapias', 'tilápia', 'tilápias'],
            'camarão inteiro gg': ['camarão inteiro', 'camarão gg', 'inteiro gg'],
            'surubim': ['surubim', 'surubins'],
            'piramutaba': ['piramutaba', 'piramutabas'],
            'bacalhau': ['bacalhau', 'bacalhaus'],
            'pescada amarela': ['pescada', 'pescada amarela', 'pescada-amarela'],
            'camarão limpo g': ['camarão limpo', 'limpo g', 'camarão g', 'limpo grande'],
            'camarão p/ molho': ['camarão p/ molho', 'camarão p molho', 'camarão para molho', 'p/ molho', 'p molho'],
            'camarão eviscerado': ['camarão eviscerado', 'eviscerado', 'camarão ev'],
            'camarão eviscerado xg': ['camarão eviscerado xg', 'eviscerado xg', 'camarão ev xg', 'ev xg'],
            'salmão': ['salmão', 'salmao', 'salmões']
        }
        
        # Criar mapeamento reverso de variações para IDs de produtos
        self.variacao_para_id = {}
        for produto in self.produtos:
            nome_lower = produto['nome'].lower()
            if nome_lower in self.variacoes:
                for variacao in self.variacoes[nome_lower]:
                    self.variacao_para_id[variacao] = produto['id']
            else:
                self.variacao_para_id[nome_lower] = produto['id']
    
    def _load_produtos(self) -> List[Dict[str, Any]]:
        """
        Carrega a lista de produtos do banco de dados.
        
        Returns:
            Lista de dicionários contendo id e nome dos produtos
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM produtos")
        produtos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return produtos
    
    def normalize_number(self, number_str: str) -> float:
        """
        Normaliza uma string de número para um float.
        
        Args:
            number_str: String contendo um número (pode ter vírgulas, pontos, etc.)
            
        Returns:
            Número convertido para float
        """
        # Remove caracteres não numéricos, exceto vírgula e ponto
        clean_str = re.sub(r'[^\d,.]', '', number_str)
        
        # Substitui vírgula por ponto (padrão brasileiro para decimal)
        clean_str = clean_str.replace(',', '.')
        
        # Se houver mais de um ponto, assume que o último é o decimal
        if clean_str.count('.') > 1:
            parts = clean_str.split('.')
            clean_str = ''.join(parts[:-1]) + '.' + parts[-1]
        
        try:
            return float(clean_str)
        except ValueError:
            return 0.0
    
    def identify_product(self, text: str) -> Optional[int]:
        """
        Identifica o produto a partir do texto usando correspondência exata ou fuzzy.
        
        Args:
            text: Texto contendo o nome do produto
            
        Returns:
            ID do produto identificado ou None se não for encontrado
        """
        text = text.lower().strip()
        
        # Verificar correspondência exata nas variações
        if text in self.variacao_para_id:
            return self.variacao_para_id[text]
        
        # Verificar correspondência parcial nas variações
        for variacao, produto_id in self.variacao_para_id.items():
            if variacao in text or text in variacao:
                return produto_id
        
        # Usar fuzzy matching como último recurso
        match = process.extractOne(
            text, 
            self.produto_nomes, 
            scorer=fuzz.token_sort_ratio, 
            score_cutoff=70
        )
        
        if match:
            nome_match = match[0]
            for produto in self.produtos:
                if produto['nome'].lower() == nome_match:
                    return produto['id']
        
        return None
    
    def parse_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Analisa uma linha de texto para extrair quantidade, unidade e produto.
        
        Args:
            line: Linha de texto a ser analisada
            
        Returns:
            Dicionário com informações do produto ou None se não for possível analisar
        """
        line = line.strip()
        if not line:
            return None
        
        # Padrão para capturar quantidade no início da linha
        # Captura números com ou sem kg, com vírgulas ou pontos
        qty_pattern = r'^([\d,.]+)(?:\s*kg)?'
        qty_match = re.match(qty_pattern, line)
        
        if not qty_match:
            return None
        
        qty_str = qty_match.group(1)
        quantidade = self.normalize_number(qty_str)
        
        # Verificar se tem unidade kg
        has_kg = 'kg' in line.lower()
        unidade = 'kg' if has_kg else 'un'
        
        # Remover a parte da quantidade e unidade para obter o nome do produto
        produto_text = re.sub(r'^[\d,.\s]+(kg)?', '', line).strip()
        
        # Casos especiais
        if 'promoção' in produto_text.lower() or 'c promoção' in produto_text.lower():
            # Verificar se é apenas "c promoção" ou "promoção" sem nome de produto
            if re.match(r'(?i)^\s*(c\s*)?promoção\s*$', produto_text):
                # Assumir que é tilápia em promoção (ID 1) - pode ser ajustado conforme necessário
                return {
                    'produto_id': 1,
                    'nome': self.produto_map[1]['nome'],
                    'quantidade': quantidade,
                    'unidade': unidade,
                    'observacao': 'Promoção'
                }
            
            produto_text = re.sub(r'(?i)(\s*c\s*promoção|\s*promoção)', '', produto_text).strip()
            
            # Se após remover "promoção" não sobrar texto, não podemos identificar o produto
            if not produto_text:
                return None
        
        produto_id = self.identify_product(produto_text)
        
        if produto_id:
            result = {
                'produto_id': produto_id,
                'nome': self.produto_map[produto_id]['nome'],
                'quantidade': quantidade,
                'unidade': unidade
            }
            
            # Adicionar observação se houver promoção no texto
            if 'promoção' in line.lower():
                result['observacao'] = 'Promoção'
                
            return result
        
        return None
    
    def parse_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Processa um texto completo contendo múltiplas linhas de produtos.
        
        Args:
            text: Texto completo a ser processado
            
        Returns:
            Lista de dicionários com informações dos produtos identificados
        """
        lines = text.strip().split('\n')
        results = []
        
        for line in lines:
            parsed = self.parse_line(line)
            if parsed:
                results.append(parsed)
        
        return results


# Função de conveniência para uso direto
def process_text(text: str, db_path: str = 'estoque.db') -> List[Dict[str, Any]]:
    """
    Processa um texto contendo lista de produtos e retorna informações estruturadas.
    
    Args:
        text: Texto a ser processado
        db_path: Caminho para o banco de dados SQLite
        
    Returns:
        Lista de dicionários com informações dos produtos identificados
    """
    processor = TextProcessor(db_path)
    return processor.parse_text(text)


if __name__ == "__main__":
    # Exemplo de uso
    sample_text = """
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
    
    results = process_text(sample_text)
    for item in results:
        output = f"Produto: {item['nome']}, Quantidade: {item['quantidade']} {item['unidade']}"
        if 'observacao' in item:
            output += f", Observação: {item['observacao']}"
        print(output)
