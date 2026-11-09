from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.physics.Vec3D import Vec3D


_PROTECTED_BLOCKS = {
    blocks.bedrock.blockID,
    blocks.oreGold.blockID,
    blocks.oreIron.blockID,
    blocks.oreDiamond.blockID,
    blocks.blockGold.blockID,
    blocks.blockSteel.blockID,
    blocks.blockDiamond.blockID,
    blocks.tnt.blockID,
    blocks.obsidian.blockID,
    blocks.chest.blockID,
    blocks.stoneOvenIdle.blockID,
    blocks.stoneOvenActive.blockID,
    blocks.luckyBlock.blockID,
    blocks.tsarBomba.blockID,
}


def findFactionTarget(entity, enemyType, searchRange=20.0):
    closest = None
    closestDistance = searchRange * searchRange
    area = entity.boundingBox.expand(searchRange, 8.0, searchRange)
    for candidate in entity._worldObj.getEntitiesWithinAABBExcludingEntity(entity, area):
        if not isinstance(candidate, enemyType) or not candidate.isEntityAlive():
            continue

        distance = entity.getDistanceSqToEntity(candidate)
        if distance < closestDistance:
            closest = candidate
            closestDistance = distance

    return closest


def breakObstructingBlock(entity, target):
    if not target or not target.isEntityAlive():
        return False

    world = entity._worldObj
    start = Vec3D(entity.posX, entity.posY + entity._getEyeHeight(), entity.posZ)
    end = Vec3D(target.posX, target.posY + target._getEyeHeight(), target.posZ)
    hit = world.rayTraceBlocks(start, end)
    if not hit:
        return False

    x, y, z = hit.blockX, hit.blockY, hit.blockZ
    if x < 0 or y < 0 or z < 0 or x >= world.width or \
       y >= world.height or z >= world.length:
        return False

    blockId = world.getBlockId(x, y, z)
    if blockId in _PROTECTED_BLOCKS:
        return False

    block = blocks.blocksList[blockId] if blockId else None
    if not block or not block.isCollidable():
        return False

    return world.setBlockWithNotify(x, y, z, 0)
