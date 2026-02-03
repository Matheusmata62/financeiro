import React from 'react'
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  FlatList,
  ActivityIndicator,
  Alert,
} from 'react-native'
import { ApiService } from '../services/ApiService'

export default function HomeScreen() {
  const [financiamentos, setFinanciamentos] = React.useState([])
  const [loading, setLoading] = React.useState(true)
  const [selectedId, setSelectedId] = React.useState(null)
  const [dados, setDados] = React.useState(null)

  React.useEffect(() => {
    carregarFinanciamentos()
  }, [])

  const carregarFinanciamentos = async () => {
    try {
      setLoading(true)
      const response = await ApiService.getFinanciamentos()
      if (response.data.success) {
        setFinanciamentos(response.data.data)
      }
    } catch (error) {
      Alert.alert('Erro', 'Falha ao carregar financiamentos')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const carregarDados = async (id) => {
    try {
      const response = await ApiService.getFinanciamento(id)
      if (response.data.success) {
        setDados(response.data.data)
        setSelectedId(id)
      }
    } catch (error) {
      Alert.alert('Erro', 'Falha ao carregar dados')
    }
  }

  const renderFinanciamento = ({ item }) => (
    <TouchableOpacity
      style={[styles.card, selectedId === item.id && styles.cardSelected]}
      onPress={() => carregarDados(item.id)}
    >
      <Text style={styles.cardTitle}>{item.nome}</Text>
      <Text style={styles.cardValue}>
        R$ {parseFloat(item.saldo_atual).toLocaleString('pt-BR', {
          style: 'currency',
          currency: 'BRL',
        })}
      </Text>
    </TouchableOpacity>
  )

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#667eea" />
      </View>
    )
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>🏍️ Financiando</Text>
        <Text style={styles.headerSubtitle}>Meus Financiamentos</Text>
      </View>

      {financiamentos.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyText}>Nenhum financiamento ainda</Text>
          <Text style={styles.emptySubText}>Crie um novo para começar</Text>
        </View>
      ) : (
        <>
          <FlatList
            data={financiamentos}
            renderItem={renderFinanciamento}
            keyExtractor={(item) => item.id.toString()}
            scrollEnabled={false}
            contentContainerStyle={styles.listContent}
          />

          {dados && (
            <View style={styles.dashboardCard}>
              <Text style={styles.dashboardTitle}>📊 Dashboard</Text>
              
              <View style={styles.metricsGrid}>
                <View style={styles.metric}>
                  <Text style={styles.metricLabel}>Saldo Atual</Text>
                  <Text style={styles.metricValue}>
                    R$ {parseFloat(dados.saldo_atual).toLocaleString('pt-BR')}
                  </Text>
                </View>

                <View style={styles.metric}>
                  <Text style={styles.metricLabel}>Meses Economizados</Text>
                  <Text style={styles.metricValue}>{dados.meses_economizados}</Text>
                </View>

                <View style={styles.metric}>
                  <Text style={styles.metricLabel}>Economia de Juros</Text>
                  <Text style={styles.metricValue}>
                    R$ {parseFloat(dados.economia_juros).toLocaleString('pt-BR')}
                  </Text>
                </View>

                <View style={styles.metric}>
                  <Text style={styles.metricLabel}>Total de Aportes</Text>
                  <Text style={styles.metricValue}>
                    R$ {parseFloat(dados.total_aportes).toLocaleString('pt-BR')}
                  </Text>
                </View>
              </View>
            </View>
          )}
        </>
      )}
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
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  headerSubtitle: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
  },
  listContent: {
    padding: 15,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
    borderWidth: 2,
    borderColor: 'transparent',
    elevation: 2,
  },
  cardSelected: {
    borderColor: '#667eea',
    backgroundColor: '#f0f0ff',
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 5,
  },
  cardValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#667eea',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#999',
    marginBottom: 5,
  },
  emptySubText: {
    fontSize: 14,
    color: '#ccc',
  },
  dashboardCard: {
    backgroundColor: '#fff',
    margin: 15,
    borderRadius: 10,
    padding: 20,
    elevation: 2,
  },
  dashboardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
    borderBottomWidth: 2,
    borderBottomColor: '#667eea',
    paddingBottom: 10,
  },
  metricsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  metric: {
    width: '48%',
    backgroundColor: '#f5f5f5',
    padding: 15,
    borderRadius: 8,
    marginBottom: 10,
    alignItems: 'center',
  },
  metricLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 5,
  },
  metricValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#667eea',
    textAlign: 'center',
  },
})
