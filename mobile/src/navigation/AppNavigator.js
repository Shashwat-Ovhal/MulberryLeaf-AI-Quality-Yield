import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator, CardStyleInterpolators } from '@react-navigation/stack';
import HomeScreen from '../screens/HomeScreen';
import AssessmentScreen from '../screens/AssessmentScreen';
import YieldScreen from '../screens/YieldScreen';
import { theme } from '../theme/theme';
import { StatusBar } from 'react-native';

const Stack = createStackNavigator();

export default function AppNavigator() {
    return (
        <NavigationContainer>
            <StatusBar barStyle="light-content" backgroundColor={theme.colors.background} />
            <Stack.Navigator
                screenOptions={{
                    headerShown: false,
                    cardStyle: { backgroundColor: theme.colors.background },
                    cardStyleInterpolator: CardStyleInterpolators.forFadeFromBottomAndroid,
                    transitionSpec: {
                        open: { animation: 'spring', config: { stiffness: 1000, damping: 100 } },
                        close: { animation: 'spring', config: { stiffness: 1000, damping: 100 } },
                    }
                }}
            >
                <Stack.Screen name="Home" component={HomeScreen} />
                <Stack.Screen name="Assessment" component={AssessmentScreen} />
                <Stack.Screen name="Yield" component={YieldScreen} />
            </Stack.Navigator>
        </NavigationContainer>
    );
}
