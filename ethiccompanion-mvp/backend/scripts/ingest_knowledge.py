#!/usr/bin/env python3
"""
Script para ingestão de conhecimento na base de dados vetorial.
Este script processa os arquivos markdown da base de conhecimento
e os prepara para uso no sistema RAG.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import json

def load_knowledge_files(knowledge_base_path: Path) -> Dict[str, str]:
    """
    Carregar todos os arquivos markdown da base de conhecimento.
    """
    knowledge_files = {}
    
    for file_path in knowledge_base_path.glob("*.md"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                knowledge_files[file_path.stem] = content
                print(f"✓ Carregado: {file_path.name}")
        except Exception as e:
            print(f"✗ Erro ao carregar {file_path.name}: {e}")
    
    return knowledge_files

def chunk_content(content: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Dividir conteúdo em chunks menores para processamento.
    """
    chunks = []
    start = 0
    
    while start < len(content):
        end = start + chunk_size
        
        # Tentar quebrar em uma nova linha para evitar cortar palavras
        if end < len(content):
            newline_pos = content.rfind('\n', start, end)
            if newline_pos != -1:
                end = newline_pos
        
        chunk = content[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks

def preprocess_content(content: str) -> str:
    """
    Preprocessar conteúdo para melhor qualidade de busca.
    """
    # Remover cabeçalhos markdown excessivos
    content = content.replace('#', '')
    
    # Normalizar espaços
    content = ' '.join(content.split())
    
    # Remover caracteres especiais desnecessários
    content = content.replace('*', '').replace('_', '')
    
    return content

def create_embeddings_data(knowledge_files: Dict[str, str]) -> List[Dict]:
    """
    Criar dados estruturados para embeddings.
    """
    embeddings_data = []
    
    for filename, content in knowledge_files.items():
        # Preprocessar conteúdo
        processed_content = preprocess_content(content)
        
        # Dividir em chunks
        chunks = chunk_content(processed_content)
        
        for i, chunk in enumerate(chunks):
            embeddings_data.append({
                "id": f"{filename}_chunk_{i}",
                "source_file": filename,
                "content": chunk,
                "metadata": {
                    "file_type": "knowledge_base",
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            })
    
    return embeddings_data

def save_processed_data(data: List[Dict], output_path: Path) -> None:
    """
    Salvar dados processados em arquivo JSON.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Dados salvos em: {output_path}")
    except Exception as e:
        print(f"✗ Erro ao salvar dados: {e}")

def main():
    """
    Função principal do script de ingestão.
    """
    print("🚀 Iniciando ingestão da base de conhecimento...")
    
    # Caminhos
    current_dir = Path(__file__).parent
    knowledge_base_path = current_dir.parent / "ethical_knowledge_base"
    output_path = current_dir / "processed_knowledge.json"
    
    # Verificar se o diretório existe
    if not knowledge_base_path.exists():
        print(f"✗ Diretório não encontrado: {knowledge_base_path}")
        sys.exit(1)
    
    # Carregar arquivos
    print(f"\n📚 Carregando arquivos de: {knowledge_base_path}")
    knowledge_files = load_knowledge_files(knowledge_base_path)
    
    if not knowledge_files:
        print("✗ Nenhum arquivo encontrado!")
        sys.exit(1)
    
    print(f"✓ {len(knowledge_files)} arquivos carregados")
    
    # Processar dados
    print("\n🔄 Processando conteúdo...")
    embeddings_data = create_embeddings_data(knowledge_files)
    
    print(f"✓ {len(embeddings_data)} chunks criados")
    
    # Salvar dados processados
    print("\n💾 Salvando dados processados...")
    save_processed_data(embeddings_data, output_path)
    
    # Estatísticas
    total_content_length = sum(len(item['content']) for item in embeddings_data)
    avg_chunk_size = total_content_length / len(embeddings_data) if embeddings_data else 0
    
    print(f"""
    📊 Estatísticas:
    - Arquivos processados: {len(knowledge_files)}
    - Total de chunks: {len(embeddings_data)}
    - Tamanho médio do chunk: {avg_chunk_size:.0f} caracteres
    - Conteúdo total: {total_content_length:,} caracteres
    """)
    
    print("✅ Ingestão concluída com sucesso!")

if __name__ == "__main__":
    main()
