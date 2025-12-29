import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ActivityIndicator, Alert } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { BlurView } from 'expo-blur';
import { theme } from '../theme/theme';
import LeafScanner from '../components/LeafScanner';
import { mulberryApi } from '../services/mulberryApi';
// import { loadTensorflowModel } from 'react-native-fast-tflite'; // FUTURE INTEGRATION

export default function AssessmentScreen({ navigation }) {
    const [isScanning, setIsScanning] = useState(false);
    const [imageUri, setImageUri] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handlePictureTaken = (photo) => {
        setIsScanning(false);
        setImageUri(photo.uri);
        analyzeImage(photo.uri);
    };

    const analyzeImage = async (uri) => {
        setLoading(true);
        try {
            // NOTE: In production, we would use TFLite here for offline inference.
            // For now, we will use the API bridge as a fallback/hybrid approach
            // checking if the model is loaded on device would go here.

            const data = await mulberryApi.predictQuality(uri);
            setResult(data);
        } catch (error) {
            Alert.alert("Error", "Failed to analyze image. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <View style={styles.container}>
            {isScanning ? (
                <LeafScanner
                    onPictureTaken={handlePictureTaken}
                    onClose={() => setIsScanning(false)}
                />
            ) : (
                <LinearGradient colors={[theme.colors.background, '#0f1f14']} style={styles.content}>
                    <View style={styles.header}>
                        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
                            <Text style={styles.backText}>←</Text>
                        </TouchableOpacity>
                        <Text style={theme.typography.h2}>Leaf Analysis</Text>
                        <View style={{ width: 30 }} />
                    </View>

                    <View style={styles.displayArea}>
                        {imageUri ? (
                            <Image source={{ uri: imageUri }} style={styles.previewImage} />
                        ) : (
                            <View style={styles.placeholder}>
                                <Text style={{ fontSize: 50 }}>🌿</Text>
                                <Text style={[theme.typography.body, { marginTop: 10 }]}>No image selected</Text>
                            </View>
                        )}
                    </View>

                    {loading && <ActivityIndicator size="large" color={theme.colors.primary} style={{ marginVertical: 20 }} />}

                    {result && !loading && (
                        <BlurView intensity={30} tint="dark" style={styles.resultCard}>
                            <Text style={[theme.typography.h2, { color: theme.colors.primary }]}>
                                {result.predicted_class || "Healthy"}
                            </Text>
                            <Text style={theme.typography.body}>
                                Confidence: {(result.confidence * 100).toFixed(1)}%
                            </Text>
                            <View style={styles.divider} />
                            <Text style={theme.typography.body}>
                                Based on the visual analysis, this leaf appears to be {result.predicted_class ? result.predicted_class.toLowerCase() : "healthy"}.
                            </Text>
                        </BlurView>
                    )}

                    <TouchableOpacity
                        style={styles.actionButton}
                        onPress={() => setIsScanning(true)}
                    >
                        <Text style={styles.actionButtonText}>{imageUri ? 'Scan Another' : 'Start Scanning'}</Text>
                    </TouchableOpacity>
                </LinearGradient>
            )}
        </View>
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
    displayArea: {
        height: 300,
        borderRadius: 24,
        overflow: 'hidden',
        backgroundColor: 'rgba(255,255,255,0.05)',
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
        marginBottom: theme.spacing.l,
    },
    previewImage: {
        width: '100%',
        height: '100%',
        resizeMode: 'cover',
    },
    placeholder: {
        alignItems: 'center',
    },
    resultCard: {
        padding: theme.spacing.l,
        borderRadius: 20,
        overflow: 'hidden',
        backgroundColor: 'rgba(46, 160, 67, 0.1)',
        borderWidth: 1,
        borderColor: 'rgba(46, 160, 67, 0.3)',
        marginBottom: theme.spacing.l,
    },
    divider: {
        height: 1,
        backgroundColor: 'rgba(255,255,255,0.1)',
        marginVertical: theme.spacing.m,
    },
    actionButton: {
        backgroundColor: theme.colors.primary,
        paddingVertical: 16,
        borderRadius: 30,
        alignItems: 'center',
        marginTop: 'auto',
        marginBottom: 20,
        shadowColor: theme.colors.primary,
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 5,
    },
    actionButtonText: {
        color: 'white',
        fontSize: 18,
        fontWeight: 'bold',
    },
});
