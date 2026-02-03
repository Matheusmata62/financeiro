import React from 'react'
import { View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, Alert } from 'react-native'
import { ApiService } from '../services/ApiService'

export default function NovoFinanciamentoScreen() {
  const [form, setForm] = React.useState({
    nome: '',
    saldo_inicial: '',
    taxa_mensal: '',
    parcela_fixa: '',
    descricao: '',
  })
  const [loading, setLoading] = React.useState(false)

  const handleChange = (field, value) => {
    setForm({ ...form, [field]: value })
  }

  const handleSubmit = async () => {
    if (!form.nome || !form.saldo_inicial || !form.taxa_mensal || !form.parcela_fixa) {
      Alert.alert('Erro', 'Preencha todos os campos obrigatórios')
      return
    }

    try {
      setLoading(true)
      const response = await ApiService.criarFinanciamento({
        nome: form.nome,
        saldo_inicial: parseFloat(form.saldo_inicial),
        taxa_mensal: parseFloat(form.taxa_mensal),
        parcela_fixa: parseFloat(form.parcela_fixa),
        descricao: form.descricao,
      })

      if (response.data.success) {
        Alert.alert('Sucesso', 'Financiamento criado com sucesso!')
        setForm({
          nome: '',
          saldo_inicial: '',
          taxa_mensal: '',
          parcela_fixa: '',
          descricao: '',
        })
      }
    } catch (error) {
      Alert.alert('Erro', 'Falha ao criar financiamento')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>➕ Novo Financiamento</Text>
      </View>

      <View style={styles.form}>
        <View style={styles.formGroup}>
          <Text style={styles.label}>Nome do Veículo *</Text>
          <TextInput
            style={styles.input}
            placeholder="Ex: Moto Honda CB 500"
            value={form.nome}
            onChangeText={(value) => handleChange('nome', value)}
          />
        </View>

        <View style={styles.formGroup}>
          <Text style={styles.label}>Saldo Inicial (R$) *</Text>
          <TextInput
            style={styles.input}
            placeholder="Ex: 15000"
            keyboardType="decimal-pad"
            value={form.saldo_inicial}
            onChangeText={(value) => handleChange('saldo_inicial', value)}
          />
        </View>

        <View style={styles.formGroup}>
          <Text style={styles.label}>Taxa Mensal (%) *</Text>
          <TextInput
            style={styles.input}
            placeholder="Ex: 1.5"
            keyboardType="decimal-pad"
            value={form.taxa_mensal}
            onChangeText={(value) => handleChange('taxa_mensal', value)}
          />
        </View>

        <View style={styles.formGroup}>
          <Text style={styles.label}>Parcela Fixa (R$) *</Text>
          <TextInput
            style={styles.input}
            placeholder="Ex: 500"
            keyboardType="decimal-pad"
            value={form.parcela_fixa}
            onChangeText={(value) => handleChange('parcela_fixa', value)}
          />
        </View>

        <View style={styles.formGroup}>
          <Text style={styles.label}>Descrição</Text>
          <TextInput
            style={[styles.input, styles.textarea]}
            placeholder="Notas adicionais..."
            multiline
            numberOfLines={4}
            value={form.descricao}
            onChangeText={(value) => handleChange('descricao', value)}
          />
        </View>

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleSubmit}
          disabled={loading}
        >
          <Text style={styles.buttonText}>
            {loading ? 'Criando...' : 'Criar Financiamento'}
          </Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#667eea',
    padding: 30,
    paddingTop: 50,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  form: {
    padding: 20,
  },
  formGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 12,
    fontSize: 16,
    color: '#333',
  },
  textarea: {
    textAlignVertical: 'top',
    paddingTop: 12,
  },
  button: {
    backgroundColor: '#667eea',
    borderRadius: 8,
    paddingVertical: 15,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
})
