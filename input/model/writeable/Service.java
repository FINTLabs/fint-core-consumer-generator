package no.fintlabs.consumer.model.MODEL_LOWER;

import lombok.extern.slf4j.Slf4j;
import no.fint.model.felles.kompleksedatatyper.Identifikator;
import no.fint.model.resource.DOMAIN.PACKAGE.MODEL_RESOURCE;
import no.fintlabs.cache.Cache;
import no.fintlabs.cache.CacheManager;
import no.fintlabs.cache.packing.PackingTypes;
import no.fintlabs.core.consumer.shared.resource.CacheService;
import no.fintlabs.core.consumer.shared.resource.ConsumerConfig;
import no.fintlabs.core.consumer.shared.resource.kafka.EntityKafkaConsumer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.nio.charset.StandardCharsets;
import java.util.Optional;

@Slf4j
@Service
public class MODELService extends CacheService<MODEL_RESOURCE> {

    private final EntityKafkaConsumer<MODEL_RESOURCE> entityKafkaConsumer;

    private final MODELLinker linker;

    private final MODELResponseKafkaConsumer MODEL_LOWERResponseKafkaConsumer;

    public MODELService(
            MODELConfig consumerConfig,
            CacheManager cacheManager,
            MODELEntityKafkaConsumer entityKafkaConsumer,
            MODELLinker linker, MODELResponseKafkaConsumer MODEL_LOWERResponseKafkaConsumer) {
        super(consumerConfig, cacheManager, entityKafkaConsumer);
        this.entityKafkaConsumer = entityKafkaConsumer;
        this.linker = linker;
        this.MODEL_LOWERResponseKafkaConsumer = MODEL_LOWERResponseKafkaConsumer;
    }

    @Override
    protected Cache<MODEL_RESOURCE> initializeCache(CacheManager cacheManager, ConsumerConfig<MODEL_RESOURCE> consumerConfig, String s) {
        return cacheManager.create(PackingTypes.POJO, consumerConfig.getOrgId(), consumerConfig.getResourceName());
    }

    @PostConstruct
    private void registerKafkaListener() {
        long retention = entityKafkaConsumer.registerListener(MODEL_RESOURCE.class, this::addResourceToCache);
        getCache().setRetentionPeriodInMs(retention);
    }

    private void addResourceToCache(ConsumerRecord<String, MODEL_RESOURCE> consumerRecord) {
        this.eventLogger.logDataRecieved();
        MODEL_RESOURCE resource = consumerRecord.value();
        if (resource == null) {
            getCache().remove(consumerRecord.key());
        } else {
            linker.mapLinks(resource);
            this.getCache().put(consumerRecord.key(), resource, linker.hashCodes(resource));
            if (consumerRecord.headers().lastHeader("event-corr-id") != null){
                String corrId = new String(consumerRecord.headers().lastHeader("event-corr-id").value(), StandardCharsets.UTF_8);
                log.debug("Adding corrId to EntityResponseCache: {}", corrId);
                MODEL_LOWERResponseKafkaConsumer.getEntityCache().add(corrId, resource);
            }
        }
    }

    @Override
    public Optional<MODEL_RESOURCE> getBySystemId(String systemId) {
        return getCache().getLastUpdatedByFilter(systemId.hashCode(),
                (resource) -> Optional
                        .ofNullable(resource)
                        .map(MODEL_RESOURCE::getSystemId)
                        .map(Identifikator::getIdentifikatorverdi)
                        .map(systemId::equals)
                        .orElse(false)
        );
    }
}
