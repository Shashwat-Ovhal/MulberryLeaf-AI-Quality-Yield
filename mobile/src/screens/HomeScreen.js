import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { theme } from '../theme/theme';
import { BlurView } from 'expo-blur';

export default function HomeScreen({ navigation }) {
    return (
        <LinearGradient
            colors={[theme.colors.background, '#0f1f14']}
            style={styles.container}
        >
            <View style={styles.header}>
                <Text style={theme.typography.h1}>Mulberry<Text style={{ color: theme.colors.primary }}>AI</Text></Text>
                <Text style={theme.typography.body}>Smart Sericulture Assistant</Text>
            </View>

            <View style={styles.menuContainer}>
                <TouchableOpacity
                    style={styles.cardContainer}
                    onPress={() => navigation.navigate('Assessment')}
                    activeOpacity={0.8}
                >
                    <BlurView intensity={20} tint="dark" style={styles.card}>
                        <View style={[styles.iconBox, { backgroundColor: 'rgba(46, 160, 67, 0.2)' }]}>
                            <Text style={styles.emoji}>🌿</Text>
                        </View>
                        <View style={styles.cardContent}>
                            <Text style={theme.typography.h2}>Leaf Assessment</Text>
                            <Text style={theme.typography.body}>Detect diseases & quality</Text>
                        </View>
                        <Text style={styles.arrow}>→</Text>
                    </BlurView>
                </TouchableOpacity>

                <TouchableOpacity
                    style={styles.cardContainer}
                    onPress={() => navigation.navigate('Yield')}
                    activeOpacity={0.8}
                >
                    <BlurView intensity={20} tint="dark" style={styles.card}>
                        <View style={[styles.iconBox, { backgroundColor: 'rgba(210, 153, 34, 0.2)' }]}>
                            <Text style={styles.emoji}>🐛</Text>
                        </View>
                        <View style={styles.cardContent}>
                            <Text style={theme.typography.h2}>Yield Prediction</Text>
                            <Text style={theme.typography.body}>Forecast cocoon output</Text>
                        </View>
                        <Text style={styles.arrow}>→</Text>
                    </BlurView>
                </TouchableOpacity>
            </View>
        </LinearGradient>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: theme.spacing.l,
    },
    header: {
        marginTop: 60,
        marginBottom: 40,
    },
    menuContainer: {
        gap: theme.spacing.l,
    },
    cardContainer: {
        borderRadius: 24,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: theme.glass.borderColor,
    },
    card: {
        padding: theme.spacing.l,
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'rgba(22, 27, 34, 0.4)',
    },
    iconBox: {
        width: 50,
        height: 50,
        borderRadius: 16,
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: theme.spacing.m,
    },
    emoji: {
        fontSize: 24,
    },
    cardContent: {
        flex: 1,
    },
    arrow: {
        color: theme.colors.textSecondary,
        fontSize: 24,
        fontWeight: 'bold',
    },
});
