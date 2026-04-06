package me.cortex.voxy.client.config;

import me.cortex.voxy.commonImpl.VoxyCommon;

/**
 * Facade for Voxy configuration.
 *
 * All values are delegated to VoxyNeoForgeConfig (TOML).
 * This class exists for compatibility with code that references VoxyConfig.CONFIG.
 *
 * Config file location: config/voxy-client.toml
 */
public class VoxyConfig {

    public static final VoxyConfig CONFIG = new VoxyConfig();

    public boolean enabled;
    public boolean enableRendering;
    public boolean ingestEnabled;
    public float sectionRenderDistance;
    public boolean cameraDistanceCulling;
    public boolean visibilityCulling;
    public int serviceThreads;
    public float subDivisionSize;
    public boolean useEnvironmentalFog;
    public boolean shaderPackFogOverride;
    public boolean dontUseEmbeddiumBuilderThreads;
    public boolean dontUseSodiumBuilderThreads;
    public int earthCurveRatio;

    private VoxyConfig() {
        this.refreshFromBackend();
    }

    private void refreshFromBackend() {
        this.enabled = VoxyNeoForgeConfig.isEnabled();
        this.enableRendering = VoxyNeoForgeConfig.isRenderingEnabled();
        this.ingestEnabled = VoxyNeoForgeConfig.isIngestEnabled();
        this.sectionRenderDistance = VoxyNeoForgeConfig.getSectionRenderDistance();
        this.cameraDistanceCulling = VoxyNeoForgeConfig.isCameraDistanceCullingEnabled();
        this.visibilityCulling = VoxyNeoForgeConfig.isVisibilityCullingEnabled();
        this.serviceThreads = VoxyNeoForgeConfig.getServiceThreads();
        this.subDivisionSize = VoxyNeoForgeConfig.getSubDivisionSize();
        this.useEnvironmentalFog = VoxyNeoForgeConfig.useEnvironmentalFog();
        this.shaderPackFogOverride = VoxyNeoForgeConfig.enableShaderPackFogOverride();
        this.dontUseEmbeddiumBuilderThreads = VoxyNeoForgeConfig.dontUseEmbeddiumBuilderThreads();
        this.dontUseSodiumBuilderThreads = this.dontUseEmbeddiumBuilderThreads;
        this.earthCurveRatio = VoxyNeoForgeConfig.getEarthCurveRatio();
    }

    private void pushToBackend() {
        VoxyNeoForgeConfig.setEnabled(this.enabled);
        VoxyNeoForgeConfig.setRenderingEnabled(this.enableRendering);
        VoxyNeoForgeConfig.setIngestEnabled(this.ingestEnabled);
        VoxyNeoForgeConfig.setSectionRenderDistance(Math.round(this.sectionRenderDistance));
        VoxyNeoForgeConfig.setCameraDistanceCullingEnabled(this.cameraDistanceCulling);
        VoxyNeoForgeConfig.setVisibilityCullingEnabled(this.visibilityCulling);
        VoxyNeoForgeConfig.setServiceThreads(this.serviceThreads);
        VoxyNeoForgeConfig.setSubDivisionSize(this.subDivisionSize);
        VoxyNeoForgeConfig.setUseEnvironmentalFog(this.useEnvironmentalFog);
        VoxyNeoForgeConfig.setShaderPackFogOverride(this.shaderPackFogOverride);
        this.dontUseEmbeddiumBuilderThreads = this.dontUseSodiumBuilderThreads;
        VoxyNeoForgeConfig.setDontUseEmbeddiumBuilderThreads(this.dontUseEmbeddiumBuilderThreads);
        VoxyNeoForgeConfig.setEarthCurveRatio(this.earthCurveRatio);
    }

    // ========== Delegated Getters ==========

    public boolean isEnabled() {
        this.refreshFromBackend();
        return this.enabled;
    }

    public boolean isRenderingEnabled() {
        this.refreshFromBackend();
        return VoxyCommon.isAvailable() && this.enabled && this.enableRendering;
    }

    public boolean isIngestEnabled() {
        this.refreshFromBackend();
        return this.ingestEnabled;
    }

    public int getSectionRenderDistance() {
        this.refreshFromBackend();
        return Math.round(this.sectionRenderDistance);
    }

    public boolean isCameraDistanceCullingEnabled() {
        this.refreshFromBackend();
        return this.cameraDistanceCulling;
    }

    public boolean isVisibilityCullingEnabled() {
        this.refreshFromBackend();
        return this.visibilityCulling;
    }

    public int getServiceThreads() {
        this.refreshFromBackend();
        return this.serviceThreads;
    }

    public float getSubDivisionSize() {
        this.refreshFromBackend();
        return this.subDivisionSize;
    }

    public boolean useEnvironmentalFog() {
        this.refreshFromBackend();
        return this.useEnvironmentalFog;
    }

    public boolean enableShaderPackFogOverride() {
        this.refreshFromBackend();
        return this.shaderPackFogOverride;
    }

    public boolean dontUseEmbeddiumBuilderThreads() {
        this.refreshFromBackend();
        return this.dontUseEmbeddiumBuilderThreads;
    }

    public int getEarthCurveRatio() {
        this.refreshFromBackend();
        return this.earthCurveRatio;
    }

    // ========== Delegated Setters ==========

    public void setEnabled(boolean value) {
        this.enabled = value;
    }

    public void setRenderingEnabled(boolean value) {
        this.enableRendering = value;
    }

    public void setIngestEnabled(boolean value) {
        this.ingestEnabled = value;
    }

    public void setSectionRenderDistance(int value) {
        this.sectionRenderDistance = value;
    }

    public void setCameraDistanceCullingEnabled(boolean value) {
        this.cameraDistanceCulling = value;
    }

    public void setVisibilityCullingEnabled(boolean value) {
        this.visibilityCulling = value;
    }

    public void setServiceThreads(int value) {
        this.serviceThreads = value;
    }

    public void setSubDivisionSize(float value) {
        this.subDivisionSize = value;
    }

    public void setUseEnvironmentalFog(boolean value) {
        this.useEnvironmentalFog = value;
    }

    public void setShaderPackFogOverride(boolean value) {
        this.shaderPackFogOverride = value;
    }

    public void setDontUseEmbeddiumBuilderThreads(boolean value) {
        this.dontUseEmbeddiumBuilderThreads = value;
        this.dontUseSodiumBuilderThreads = value;
    }

    public void setEarthCurveRatio(int value) {
        this.earthCurveRatio = value;
    }

    // ========== Save ==========

    /**
     * Save config to TOML file.
     */
    public void save() {
        this.pushToBackend();
        VoxyNeoForgeConfig.save();
    }
}
