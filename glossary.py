# -*- coding: utf-8 -*-
import requests
import json
import string
import os

def save_glossary():
	os.system('touch buffer_response_atlas.json')
	arquivo = open('input_glossarios.json','r')
	response_glossario = open('atlas_response_glossario.json','a')
	for linha in arquivo:
		linha = linha.rstrip()
		print linha
		linha_json_glossario = json.loads(linha)
		nome_glossario = linha_json_glossario.get("name")
		print "Atributo do json de glossario: "+nome_glossario
		response = requests.post('http://10.100.16.58:21000/api/atlas/v2/glossary', auth=('admin', 'hortonworks1'), headers={'Content-Type': 'application/json'}, json=linha_json_glossario)
		#print response.status_code  # 200 significa requisição OK
		a = response.json()

		print "\nLinha do json de glossario: "
		print linha_json_glossario
		print a

		with open('atlas_response_glossario.json', 'w') as outfile:
			json.dump(a, outfile)
		#pegando o id do glossario para vincular na categoria
		response_glossario = open('atlas_response_glossario.json', 'r')
		for linha_response_glossario in response_glossario:
			linha_response_glossario = linha_response_glossario.rstrip()
			linha_response_glossario_json = json.loads(linha_response_glossario)
			guid_glossario = linha_response_glossario_json.get("guid")
			print "guid do glossario"
			print guid_glossario
			dados_glossario = [nome_glossario, guid_glossario]
		response_glossario.close()
		os.system('rm buffer_response_atlas.json')
		return dados_glossario

def update_category():
	print "prestes a atualizar a categoria - Beta version"

def save_categories(glossary):
	os.system('touch buffer_response_atlas.json')
	with open('atlas_response_glossario.json', 'w') as outfile:
		json.dump('\n', outfile)

	print "Dados da lista Glossary:"
	print glossary[0]
	print glossary[1]
	print "\n"

	#abrindo o json das categorias para verificar quais pertencem a qual glossario
	arquivo_categorias = open('input_categorias.json','r')
	for linha_categorias in arquivo_categorias:
		linha_categorias = linha_categorias.rstrip()
		print "\nLinha do json de categorias: "
		print linha_categorias
		linha_json_categorias = json.loads(linha_categorias)
		qualified_name = linha_json_categorias.get("qualifiedName")
		name = linha_json_categorias.get("displayName")
		parent_id = linha_json_categorias["parentCategory"]["categoryGuid"]
		
		#Verifica se a categoria pertence ao glossario pois procura o nome do glossario no qualifiedName da categoria: "qualifiedName":"sub-cat-gloss01@gloss01"
		if (glossary[0] in qualified_name):
			guid_glossary = glossary[1]
			
			print qualified_name
			print name
			print guid_glossary
			print "Parent Category "+ str(parent_id)

			categoria_atualizada = '{"guid":"","qualifiedName":"'+ qualified_name +'","name":"'+ name +'","anchor":{"glossaryGuid":"'+ guid_glossary +'","relationGuid":""} }'
			# print "\n essa é a categoria atualizada: \n"
			# print categoria_atualizada
			#verificar se a categoria tem pai
			if (not parent_id):
				print "Essa categoria não tem um pai"
				categoria_atualizada_file = open('input_categorias_atualizadas.json', 'a')
				buffer_response = open('buffer_response_atlas.json', 'a')
				print "**CATEGORIA ATUALIZADA**"
				print categoria_atualizada
				categoria_atualizada = json.loads(categoria_atualizada)
	    			json.dump(categoria_atualizada, categoria_atualizada_file)
	    			categoria_atualizada_file.write('\n')
	    			print categoria_atualizada
	    			response2 = requests.post('http://10.100.16.58:21000/api/atlas/v2/glossary/category', auth=('admin', 'hortonworks1'), headers={'Content-Type': 'application/json'}, json=categoria_atualizada)
	    			b = response2.json()
	    			json.dump(b, buffer_response)
	    			buffer_response.write('\n')
	    			print "\n"
					
			else:
				print "***Essa tem um pai***"
				print "parent_id: "
				print parent_id

				buffer_de_categorias_inseridas = open('buffer_response_atlas.json', 'r')
				for linha_buffer_de_categorias_inseridas in buffer_de_categorias_inseridas:
					linha_buffer_de_categorias_inseridas = linha_buffer_de_categorias_inseridas.rstrip()
					linha_buffer_de_categorias_inseridas_json = json.loads(linha_buffer_de_categorias_inseridas)
					nome_pai_categoria 	= linha_buffer_de_categorias_inseridas_json.get("name")
					qualified_name_pai 	= linha_buffer_de_categorias_inseridas_json.get("qualifiedName")
					guid_pai_categoria 	= linha_buffer_de_categorias_inseridas_json.get("guid")
					relation_guid 		= linha_buffer_de_categorias_inseridas_json["anchor"]["relationGuid"]

					if (parent_id == nome_pai_categoria):
						#subcategoria_atualizada = '{"guid":"","qualifiedName":"'+qualified_name+'","name":"'+name+'","anchor":{"glossaryGuid":"'+guid_glossary+'","relationGuid":"'+relation_guid+'"},"parentCategory":{"categoryGuid":"'+guid_pai_categoria+'","relationGuid":""} }'
						subcategoria_atualizada = '{"name":"'+ name +'","anchor":{"glossaryGuid":"'+ guid_glossary +'","relationGuid":""}, "parentCategory":{"categoryGuid":"'+guid_pai_categoria+'"}}'
						print "O pai da categoria é, "
						print nome_pai_categoria
						print subcategoria_atualizada

						subcategoria_atualizada_file = open('input_categorias_atualizadas.json', 'a')
						buffer_response = open('buffer_response_atlas.json', 'a')
						subcategoria_atualizada = json.loads(subcategoria_atualizada)
			    			json.dump(subcategoria_atualizada, subcategoria_atualizada_file)
			    			subcategoria_atualizada_file.write('\n')
			    			print subcategoria_atualizada
			    			
			    			x = requests.post('http://10.100.16.58:21000/api/atlas/v2/glossary/category', auth=('admin', 'hortonworks1'), headers={'Content-type': 'application/json'}, json=subcategoria_atualizada)
			    			y = x.json()
			    			json.dump(y, buffer_response)
			    			buffer_response.write('\n')
						#update_category()
		else:
			print "glossario nao esta em categoria"
	arquivo_categorias.close()	
	print"**FINISHED**"


def save_terms():
	print "salvar termos"
	input_termos = open('input_termos.json','r')
	response_termos = open('response_termos.json','a')
	for linha in input_termos:
		linha = linha.rstrip()
		print linha
		linha_json_termos = json.loads(linha)
		nome_termo = linha_json_termos.get("name")
		print nome_termo


#glossario = save_glossary()
#save_categories(glossario)

save_terms()