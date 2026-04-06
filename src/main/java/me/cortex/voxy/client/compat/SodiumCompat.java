package me.cortex.voxy.client.compat;

import me.cortex.voxy.client.mixin.sodium.AccessorSodiumWorldRenderer;
import net.caffeinemc.mods.sodium.client.render.SodiumWorldRenderer;

public class SodiumCompat implements RendererCompat {
    @Override
    public int getBuilderThreadCount() {
        var renderer = SodiumWorldRenderer.instanceNullable();
        if (renderer == null) {
            return -1;
        }
        var rsm = ((AccessorSodiumWorldRenderer) renderer).getRenderSectionManager();
        if (rsm == null) {
            return -1;
        }
        return rsm.getBuilder().getTotalThreadCount();
    }
}
