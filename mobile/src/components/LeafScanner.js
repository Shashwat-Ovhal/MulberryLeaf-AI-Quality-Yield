import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Text, TouchableOpacity } from 'react-native';
import { Camera } from 'expo-camera';
import { LinearGradient } from 'expo-linear-gradient';
import { theme } from '../theme/theme';
import { Ionicons } from '@expo/vector-icons'; // Assuming Ionicons is available in Expo by default or I'll use text

export default function LeafScanner({ onPictureTaken, onClose }) {
    const [hasPermission, setHasPermission] = useState(null);
    const [cameraRef, setCameraRef] = useState(null);

    useEffect(() => {
        (async () => {
            const { status } = await Camera.requestCameraPermissionsAsync();
            setHasPermission(status === 'granted');
        })();
    }, []);

    const takePicture = async () => {
        if (cameraRef) {
            const photo = await cameraRef.takePictureAsync({
                quality: 0.8,
                base64: true,
            });
            onPictureTaken(photo);
        }
    };

    if (hasPermission === null) {
        return <View style={styles.container} />;
    }
    if (hasPermission === false) {
        return <Text style={{ color: theme.colors.text }}>No access to camera</Text>;
    }

    return (
        <View style={styles.container}>
            <Camera style={styles.camera} ref={setCameraRef}>
                <LinearGradient
                    colors={['rgba(0,0,0,0.6)', 'transparent', 'rgba(0,0,0,0.6)']}
                    style={styles.overlay}
                >
                    <View style={styles.header}>
                        <TouchableOpacity onPress={onClose} style={styles.closeButton}>
                            <Text style={styles.closeText}>✕</Text>
                        </TouchableOpacity>
                        <Text style={styles.title}>Scan Leaf</Text>
                        <View style={{ width: 40 }} />
                    </View>

                    <View style={styles.scanFrame} />
                    <Text style={styles.instruction}>Align leaf within the frame</Text>

                    <View style={styles.footer}>
                        <TouchableOpacity style={styles.captureButton} onPress={takePicture}>
                            <View style={styles.captureInner} />
                        </TouchableOpacity>
                    </View>
                </LinearGradient>
            </Camera>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: 'black',
    },
    camera: {
        flex: 1,
    },
    overlay: {
        flex: 1,
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: theme.spacing.xl,
    },
    header: {
        flexDirection: 'row',
        width: '100%',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginTop: 40,
    },
    closeButton: {
        padding: 10,
        backgroundColor: 'rgba(255,255,255,0.2)',
        borderRadius: 20,
    },
    closeText: {
        color: 'white',
        fontSize: 18,
        fontWeight: 'bold',
    },
    title: {
        color: 'white',
        fontSize: 18,
        fontWeight: '600',
    },
    scanFrame: {
        width: 250,
        height: 250,
        borderWidth: 2,
        borderColor: theme.colors.primary,
        borderRadius: 20,
        backgroundColor: 'rgba(46, 160, 67, 0.1)',
    },
    instruction: {
        color: theme.colors.textSecondary,
        marginTop: theme.spacing.m,
    },
    footer: {
        marginBottom: 40,
    },
    captureButton: {
        width: 80,
        height: 80,
        borderRadius: 40,
        backgroundColor: 'rgba(255,255,255,0.3)',
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 4,
        borderColor: 'white',
    },
    captureInner: {
        width: 60,
        height: 60,
        borderRadius: 30,
        backgroundColor: 'white',
    },
});
