import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, KeyboardAvoidingView, Platform, ScrollView, Alert } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { BlurView } from 'expo-blur';
import { theme } from '../theme/theme';
import { mulberryApi } from '../services/mulberryApi';

export default function YieldScreen({ navigation, route }) {
    const { qualityScore } = route.params || {};

    const [quality, setQuality] = useState(qualityScore ? String(qualityScore) : '');
    const [temp, setTemp] = useState('');
    const [humidity, setHumidity] = useState('');
    const [loading, setLoading] = useState(false);
    const [prediction, setPrediction] = useState(null);

    // Update quality if passed via params later (optional, but good if reusing screen)
    React.useEffect(() => {
        if (qualityScore) {
            setQuality(String(qualityScore));
        }
    }, [qualityScore]);

    const handlePredict = async () => {
        if (!quality || !temp || !humidity) {
            Alert.alert("Missing Data", "Please fill in all fields.");
            return;
        }

        setLoading(true);
        try {
            const yieldVal = await mulberryApi.predictYield(
                parseFloat(quality),
                parseFloat(temp),
                parseFloat(humidity)
            );
            setPrediction(yieldVal);
        } catch (error) {
            Alert.alert("Error", "Failed to get prediction.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === "ios" ? "padding" : "height"}
            style={styles.container}
        >
            <LinearGradient colors={[theme.colors.background, '#1a140f']} style={styles.content}>
                <View style={styles.header}>
                    <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
                        <Text style={styles.backText}>←</Text>
                    </TouchableOpacity>
                    <Text style={theme.typography.h2}>Yield Prediction</Text>
                    <View style={{ width: 30 }} />
                </View>

                <ScrollView showsVerticalScrollIndicator={false}>
                    <Text style={[theme.typography.body, { marginBottom: 20 }]}>
                        Enter environmental conditions to forecast cocoon yield.
                    </Text>

                    <BlurView intensity={20} tint="dark" style={styles.formCard}>
                        <View style={styles.inputGroup}>
                            <Text style={styles.label}>Leaf Quality Score (0-1)</Text>
                            <TextInput
                                style={styles.input}
                                keyboardType="numeric"
                                placeholder="0.85"
                                placeholderTextColor="#4A5568"
                                value={quality}
                                onChangeText={setQuality}
                            />
                        </View>

                        <View style={styles.inputGroup}>
                            <Text style={styles.label}>Temperature (°C)</Text>
                            <TextInput
                                style={styles.input}
                                keyboardType="numeric"
                                placeholder="25.5"
                                placeholderTextColor="#4A5568"
                                value={temp}
                                onChangeText={setTemp}
                            />
                        </View>

                        <View style={styles.inputGroup}>
                            <Text style={styles.label}>Humidity (%)</Text>
                            <TextInput
                                style={styles.input}
                                keyboardType="numeric"
                                placeholder="65"
                                placeholderTextColor="#4A5568"
                                value={humidity}
                                onChangeText={setHumidity}
                            />
                        </View>
                    </BlurView>

                    {prediction !== null && (
                        <BlurView intensity={30} tint="dark" style={styles.resultCard}>
                            <Text style={theme.typography.body}>Predicted Yield</Text>
                            <Text style={styles.resultValue}>{prediction.toFixed(2)} kg</Text>
                        </BlurView>
                    )}

                    <TouchableOpacity
                        style={styles.predictButton}
                        onPress={handlePredict}
                        disabled={loading}
                    >
                        <Text style={styles.buttonText}>{loading ? 'Calculating...' : 'Calculate Yield'}</Text>
                    </TouchableOpacity>
                </ScrollView>
            </LinearGradient>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: theme.colors.background,
    },
    content: {
        flex: 1,
        padding: theme.spacing.l,
    },
    header: {
        marginTop: 40,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: 20,
    },
    backButton: {
        padding: 10,
        backgroundColor: 'rgba(255,255,255,0.1)',
        borderRadius: 12,
    },
    backText: {
        color: 'white',
        fontSize: 18,
    },
    formCard: {
        padding: theme.spacing.l,
        borderRadius: 24,
        overflow: 'hidden',
        backgroundColor: 'rgba(255,255,255,0.03)',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
        marginBottom: theme.spacing.l,
    },
    inputGroup: {
        marginBottom: theme.spacing.m,
    },
    label: {
        color: theme.colors.textSecondary,
        marginBottom: 8,
        fontSize: 14,
    },
    input: {
        backgroundColor: 'rgba(0,0,0,0.3)',
        borderRadius: 12,
        padding: 16,
        color: 'white',
        fontSize: 16,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    predictButton: {
        backgroundColor: theme.colors.secondary, // Different accent for yield
        paddingVertical: 18,
        borderRadius: 30,
        alignItems: 'center',
        marginTop: 10,
        shadowColor: theme.colors.secondary,
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 5,
    },
    buttonText: {
        color: 'white',
        fontSize: 18,
        fontWeight: 'bold',
    },
    resultCard: {
        padding: theme.spacing.l,
        borderRadius: 20,
        alignItems: 'center',
        backgroundColor: 'rgba(210, 153, 34, 0.1)',
        borderColor: 'rgba(210, 153, 34, 0.3)',
        borderWidth: 1,
        marginBottom: theme.spacing.l,
        overflow: 'hidden'
    },
    resultValue: {
        fontSize: 36,
        fontWeight: 'bold',
        color: '#D29922', // Gold/Yellow
        marginTop: 8,
    }
});
