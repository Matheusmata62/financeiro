import React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
import { Ionicons } from '@expo/vector-icons'

import HomeScreen from './screens/HomeScreen'
import NovoFinanciamentoScreen from './screens/NovoFinanciamentoScreen'

const Stack = createNativeStackNavigator()
const Tab = createBottomTabNavigator()

function HomeStackNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
      }}
    >
      <Stack.Screen name="HomeList" component={HomeScreen} />
    </Stack.Navigator>
  )
}

function NovoStackNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
      }}
    >
      <Stack.Screen name="NovoFinanciamentoList" component={NovoFinanciamentoScreen} />
    </Stack.Navigator>
  )
}

export default function Navigation() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName

            if (route.name === 'Home') {
              iconName = focused ? 'home' : 'home-outline'
            } else if (route.name === 'Novo') {
              iconName = focused ? 'add-circle' : 'add-circle-outline'
            } else if (route.name === 'Aportes') {
              iconName = focused ? 'cash' : 'cash-outline'
            } else if (route.name === 'Simulador') {
              iconName = focused ? 'calculator' : 'calculator-outline'
            }

            return <Ionicons name={iconName} size={size} color={color} />
          },
          tabBarActiveTintColor: '#667eea',
          tabBarInactiveTintColor: '#999',
          headerShown: false,
        })}
      >
        <Tab.Screen
          name="Home"
          component={HomeStackNavigator}
          options={{
            title: 'Dashboard',
          }}
        />
        <Tab.Screen
          name="Novo"
          component={NovoStackNavigator}
          options={{
            title: 'Novo',
          }}
        />
        <Tab.Screen
          name="Aportes"
          component={HomeStackNavigator}
          options={{
            title: 'Aportes',
          }}
        />
        <Tab.Screen
          name="Simulador"
          component={HomeStackNavigator}
          options={{
            title: 'Simulador',
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  )
}
